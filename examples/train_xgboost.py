from modelling.utils.data import load_unified_data, SEED
import numpy as np
from snapper_ml import job, AutologgingBackend, Trial, DataLoader
from snapper_ml.integrations import XGBoostPruningCallback
import xgboost as xgb
from xgboost.callback import print_evaluation


@job(data_loader_func=load_unified_data,
     autologging_backends=AutologgingBackend.XGBOOST)
def main(n_estimators: int,
         learning_rate: float,
         max_depth: int,
         gamma: float,
         subsample: float,
         min_child_weight: float):
    np.random.seed(SEED)

    X_train, X_val, y_train, y_val = DataLoader.load_data()
    train_data = xgb.DMatrix(X_train, label=y_train)
    val_data = xgb.DMatrix(X_val, label=y_val)

    params = dict(random_state=SEED,
                  learning_rate=learning_rate,
                  max_depth=max_depth,
                  gamma=gamma,
                  subsample=subsample,
                  min_child_weight=min_child_weight,
                  num_class=len(np.unique(y_train)),
                  objective='multi:softmax')

    trial = Trial.get_current()
    evallist = [(val_data, 'eval'), (train_data, 'train')]
    eval_result = {}
    patience = max(10, n_estimators // 10)

    callbacks = [
        XGBoostPruningCallback(trial, 'eval-merror'),
        xgb.callback.early_stop(patience, verbose=False),
        xgb.callback.record_evaluation(eval_result)
    ]

    xgb.train(params,
              train_data,
              num_boost_round=n_estimators,
              evals=evallist,
              callbacks=callbacks,
              verbose_eval=False)

    accuracy = 1 - eval_result['eval']['merror'][-1]
    return {'val_accuracy': accuracy}


if __name__ == '__main__':
    main()
