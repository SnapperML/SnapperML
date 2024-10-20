// Terminal.tsx
import { useEffect, useRef, useImperativeHandle, forwardRef } from "react";
import axios, { AxiosError } from "axios";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import "xterm/css/xterm.css";
import "./Terminal.css";

interface TerminalProps {
  command: string;
  output: string;
}

const TerminalComponent = forwardRef((_: TerminalProps, ref) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const xterm = useRef<Terminal | null>(null);
  const fitAddon = useRef<FitAddon | null>(null);

  let inputBuffer = "";

  useEffect(() => {
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
      xterm.current?.write("\n $ ");

      // Handle user input
      xterm.current.onData((data) => {
        handleInput(data);
      });

      return () => {
        xterm.current?.dispose();
      };
    }
  }, []);

  // Define writeOutput so it's accessible within the component
  const writeOutput = (result: string, dataStream: boolean) => {
    const lines = result.split("\n");
    lines.forEach((line, index) => {
      // Write the line to the terminal without adding a newline for the last line
      if (index === lines.length - 1) {
        xterm.current?.write(`   ${line}\r`); // No newline for the last line
      } else {
        xterm.current?.write(`   ${line}\n`); // Add newline for other lines
      }
    });

    if (!dataStream) xterm.current?.write(" $ "); // Reset the prompt
  };

  // Expose methods to parent component
  useImperativeHandle(ref, () => ({
    writeOutput,
    writeCommand: (command: string) => {
      xterm.current?.write(`${command}\n`);
    },
  }));

  const handleInput = async (input: string) => {
    const arrowKeyCodes = ["\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D"];

    if (input === "\r") {
      // Enter key pressed
      xterm.current?.write("\r\n"); // Move to the next line
      try {
        const response = await axios.post<{ output: string }>(
          "http://localhost:8000/execute",
          {
            command: inputBuffer,
          }
        );
        inputBuffer = ""; // Clear input buffer
        writeOutput(response.data.output, false); // Assume command execution ends here
      } catch (error) {
        inputBuffer = "";
        const axiosError = error as AxiosError;
        console.error("Error executing command:", axiosError);
        writeOutput("API is not reachable", false);
      }
    } else if (input === "\x7f") {
      // Backspace key pressed
      if (inputBuffer.length > 0) {
        inputBuffer = inputBuffer.slice(0, -1);
        xterm.current?.write("\b \b");
      }
    } else if (!arrowKeyCodes.includes(input)) {
      // Other keys
      inputBuffer += input;
      xterm.current?.write(input);
    }
  };

  return <div ref={terminalRef} />;
});

export default TerminalComponent;
