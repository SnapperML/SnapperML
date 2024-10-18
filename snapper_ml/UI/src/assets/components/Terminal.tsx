// Terminal.tsx
import React, { useEffect, useRef } from "react";
import axios, { AxiosError } from "axios";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import "xterm/css/xterm.css";
import "./Terminal.css";

interface TerminalProps {
  command: string; // The command to execute
  output: string; // The output to display
}

const TerminalComponent: React.FC<TerminalProps> = ({ command, output }) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const xterm = useRef<Terminal | null>(null);
  const fitAddon = useRef<FitAddon | null>(null);

  useEffect(() => {
    // Initialize the terminal
    xterm.current = new Terminal({
      cursorBlink: true,
      theme: {
        background: "#1e1e1e",
        foreground: "#dcdcdc",
      },
    });

    fitAddon.current = new FitAddon();

    if (terminalRef.current) {
      xterm.current.loadAddon(fitAddon.current);
      xterm.current.open(terminalRef.current);
      fitAddon.current.fit();
      xterm.current?.write("\r\n\x1b[34m $ ");
      // Handle user input
      xterm.current.onData((data) => {
        handleInput(data);
      });

      // Handle resize
      window.addEventListener("resize", () => {
        fitAddon.current?.fit();
      });

      return () => {
        // Clean up on component unmount
        window.removeEventListener("resize", () => {
          fitAddon.current?.fit();
        });
      };
    }
  }, []);

  useEffect(() => {
    if (command && output) {
      executeCommand(command, output);
    }
  }, [command, output]);

  let inputBuffer = "";

  const handleInput = async (input: string) => {
    if (input === "\r") {
      // Enter key
      console.log("Input submitted:", inputBuffer);
      try {
        // Call the backend API to execute the command
        const response = await axios.post<TerminalProps>(
          "http://localhost:5000/execute",
          {
            command: inputBuffer,
          }
        );
        xterm.current?.write("\r\n\x1b[34m");
        xterm.current?.write(`   \x1b[32m${response.data.output}\x1b[0m\r\n`); // Output in green
        xterm.current?.write("\r\x1b[34m $ "); // Reset the prompt

        inputBuffer = "";
      } catch (error) {
        const axiosError = error as AxiosError;
        console.error("Error executing command:", axiosError);
        xterm.current?.write("Execution failed!");
      }
    } else if (input === "\x7f") {
      // Handle backspace
      if (inputBuffer.length > 0) {
        // Remove the last character from inputBuffer
        inputBuffer = inputBuffer.slice(0, -1);
        // Move the cursor back, overwrite the character with a space, then move back again
        xterm.current?.write("\b \b");
      }
    } else {
      inputBuffer += input;
      xterm.current?.write(input); // Write other characters to the terminal
    }
  };

  const executeCommand = (cmd: string, result: string) => {
    // Write the command in blue (34m)
    xterm.current?.write(`\r\n\x1b[34m $ ${cmd}\x1b[0m\r\n`); // Command in blue

    // Write the output in green (32m)
    xterm.current?.write(`   \x1b[32m${result}\x1b[0m\r\n`); // Output in green

    // Reset the prompt for next input
    xterm.current?.write("\r\x1b[34m $ ");
  };

  return <div ref={terminalRef} className="terminal" />;
};

export default TerminalComponent;
