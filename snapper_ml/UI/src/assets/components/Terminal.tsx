import { useEffect, useRef, useImperativeHandle, forwardRef } from "react";
import { Terminal } from "@xterm/xterm";
import { FitAddon } from "@xterm/addon-fit";
import "@xterm/xterm/css/xterm.css";

interface TerminalProps {
  command: string;
  output: string;
}

const TerminalComponent = forwardRef((_: TerminalProps, ref) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const xterm = useRef<Terminal | null>(null);
  const fitAddon = useRef<FitAddon | null>(null);
  let inputBuffer = "";

  const isResetOrClearCommand = () => {
    return inputBuffer === "reset" || inputBuffer === "clear";
  };

  useEffect(() => {
    initializeTerminal();
    return () => cleanupTerminal();
  }, []);

  const initializeTerminal = () => {
    xterm.current = new Terminal({
      cursorBlink: true,
      convertEol: true,
      cursorStyle: "block",
      theme: {
        background: "#1e1e1e",
        foreground: "#dcdcdc",
      },
      rows: 49,
    });

    fitAddon.current = new FitAddon();
    if (terminalRef.current) {
      xterm.current.loadAddon(fitAddon.current);
      xterm.current.open(terminalRef.current);
      fitAddon.current.fit();
      xterm.current.write("\n $ ");
      xterm.current.onData(handleInput);
      terminalRef.current.addEventListener("wheel", preventScroll);
    }
  };

  const cleanupTerminal = () => {
    terminalRef.current?.removeEventListener("wheel", preventScroll);
    xterm.current?.dispose();
  };

  const preventScroll = (event: WheelEvent) => {
    const terminalElement = terminalRef.current;
    if (terminalElement) {
      const { scrollTop, scrollHeight, clientHeight } = terminalElement;
      const isAtTop = scrollTop === 0 && event.deltaY < 0;
      const isAtBottom =
        scrollTop + clientHeight === scrollHeight && event.deltaY > 0;
      if (isAtTop || isAtBottom) event.preventDefault();
    }
  };

  const handleInput = async (input: string) => {
    const arrowKeyCodes = ["\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D"];
    if (input === "\r") {
      await executeCommand();
    } else if (input === "\x7f") {
      handleBackspace();
    } else if (!arrowKeyCodes.includes(input)) {
      inputBuffer += input;
      xterm.current?.write(input);
    }
  };

  const handleBackspace = () => {
    if (inputBuffer.length > 0) {
      inputBuffer = inputBuffer.slice(0, -1);
      xterm.current?.write("\b \b");
    }
  };

  const executeCommand = async () => {
    xterm.current?.write("\r\n");
    if (!inputBuffer) {
      xterm.current?.write(" $ ");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cmd: inputBuffer }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder("utf-8");

      if (reader) {
        await processResponse(reader, decoder);
      }

      if (isResetOrClearCommand()) {
        xterm.current?.write("\n\r $ ");
      }

      inputBuffer = "";
    } catch (error) {
      inputBuffer = "";
      console.error("Error executing command:", error);
      writeOutput("API not reachable.\n", false);
    }
  };

  const processResponse = async (
    reader: ReadableStreamDefaultReader<Uint8Array>,
    decoder: TextDecoder
  ) => {
    let done = false;
    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      let chunk = decoder.decode(value);
      chunk = chunk.replace(/\nPROCESS_STATUS: (True|False)\n/, "");
      writeOutput(chunk, !done || isResetOrClearCommand());
    }
  };

  const writeOutput = (result: string, dataStream: boolean) => {
    const lines = result.split("\n");
    lines.forEach((line, index) => {
      const formattedLine = `   ${line}${
        index === lines.length - 1 ? "\r" : "\n"
      }`;
      xterm.current?.write(formattedLine);
    });
    if (!dataStream) xterm.current?.write(" $ ");
  };

  useImperativeHandle(ref, () => ({
    writeOutput,
    writeCommand: (command: string) => {
      xterm.current?.write(`${command}\n`);
    },
  }));

  return <div ref={terminalRef} />;
});

export default TerminalComponent;
