// Terminal.tsx
import React, { useEffect, useRef } from "react";
import axios, { AxiosError } from "axios";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import "xterm/css/xterm.css";
import "./Terminal.css";

interface TerminalProps {
  command: string;
  output: string;
}

const TerminalComponent: React.FC<TerminalProps> = ({ command, output }) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const xterm = useRef<Terminal | null>(null);
  const fitAddon = useRef<FitAddon | null>(null);

  useEffect(() => {
    // Initialize the terminal
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
      // Prevent the website from scrolling when reaching the top or bottom of the terminal
      const preventScroll = (event: WheelEvent) => {
        const terminalElement = terminalRef.current;
        if (terminalElement) {
          const { scrollTop, scrollHeight, clientHeight } = terminalElement;
          const isAtTop = scrollTop === 0 && event.deltaY < 0;
          const isAtBottom =
            scrollTop + clientHeight === scrollHeight && event.deltaY > 0;

          if (isAtTop || isAtBottom) {
            event.preventDefault();
          }
        }
      };

      terminalRef.current.addEventListener("wheel", preventScroll);

      // Clean up event listener when the component is unmounted
      return () => {
        terminalRef.current?.removeEventListener("wheel", preventScroll);
        xterm.current?.dispose();
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
    // Ignore arrow keys (up, down, left, right)
    const arrowKeyCodes = ["\x1b[A", "\x1b[B", "\x1b[C", "\x1b[D"]; // Escape sequences for arrow keys

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
        inputBuffer = "";
        executeCommand("", response.data.output);
      } catch (error) {
        inputBuffer = "";
        const axiosError = error as AxiosError;
        console.error("Error executing command:", axiosError);
        executeCommand("", "API is not reachable");
      }
    } else if (input === "\x7f") {
      // Handle backspace
      if (inputBuffer.length > 0) {
        // Remove the last character from inputBuffer
        inputBuffer = inputBuffer.slice(0, -1);
        // Move the cursor back, overwrite the character with a space, then move back again
        xterm.current?.write("\b \b");
      }
    } else if (!arrowKeyCodes.includes(input)) {
      // Ignore arrow key inputs
      inputBuffer += input;
      xterm.current?.write(input); // Write other characters to the terminal
    }
  };

  const executeCommand = (cmd: string, result: string) => {
    // Write the command
    xterm.current?.write(`${cmd}\n`);

    // Split the result into lines and write each line
    const lines = result.split("\n");
    lines.forEach((line) => {
      xterm.current?.write(`   ${line}\n`);
    });

    // Reset the prompt for next input
    xterm.current?.write(" $ ");
  };

  return <div ref={terminalRef} />;
};

export default TerminalComponent;
