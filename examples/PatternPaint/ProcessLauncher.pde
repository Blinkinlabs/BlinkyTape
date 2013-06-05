import java.util.concurrent.*;

// Thread code from here:
// http://stackoverflow.com/questions/3343066/reading-streams-from-java-runtime-exec

class ProcessLauncher {

  // Our process
  private Process shell;

  // readers and writer to talk to the process
  private java.io.BufferedReader stdOut;
  private java.io.BufferedReader stdErr;
  private java.io.BufferedWriter stdIn;

  // Queue of strings that we maintain, that are going to and from the process
  private LinkedBlockingQueue inputQueue = new LinkedBlockingQueue();
  private LinkedBlockingQueue outputQueue = new LinkedBlockingQueue();

  ProcessLauncher(String interpreter) {

    // Open the shell
    try {
      shell = Runtime.getRuntime().exec(interpreter, null, new File(sketchPath("")));
    }
    catch(Exception e) {
      println(e);
      // TODO: Fail her
    }

    // Make input and output stream readers that are connected to the process    
    stdOut = new java.io.BufferedReader(new java.io.InputStreamReader(shell.getInputStream()));
    stdErr = new java.io.BufferedReader(new java.io.InputStreamReader(shell.getErrorStream()));
    stdIn  = new java.io.BufferedWriter(new java.io.OutputStreamWriter(shell.getOutputStream()));

    // launch a thread to read data from the process
    // It basically blocks until there is data available in stdout, then puts that data
    // into a threadsafe queue for the main thread to handle.
    new Thread() {
      public void run() {
        try { 
          while (true) {

            String line;

            while ( (line = stdOut.readLine ()) != null) {
//              try {
                outputQueue.put(line);
//              }
//              catch( InterruptedException e ) {
//                println("Interrupted Exception caught");
//              }

              print(line + '\n');
            }
            delay(100); // a kludge?
          }
        }
        catch (Exception e) {
          println("stdout exception!");
          throw new Error(e);
        }
      }
    }
    .start(); // Starts now

    // launch a thread to read err from the process
    // It basically blocks until there is data available in stderr, then puts that data
    // into a threadsafe queue for the main thread to handle.
    new Thread() {
      public void run() {
        try {
          while (true) {
            String line;

            while ( (line = stdErr.readLine ()) != null) {
              outputQueue.put(line);
              print(line + '\n');
            }
            
            delay(100); // TODO: a crutch?
          }
        }
        catch (Exception e) {
          println("stderr exception!");
          throw new Error(e);
        }
      }
    }
    .start(); // Starts now


    // and another thread to give data to the process
    // It basically blocks until there is data available in the input queue, then sends that
    // data to the process for consumption.
    new Thread() {
      public void run() {
        try {
          while (true) {
            String in = (String)inputQueue.take();
            print("sending: " + in + "\n");
            stdIn.write(in + "\n");

            delay(100); // TODO: a crutch?

            stdIn.flush();
          }
        }
        catch (Exception e) {
          println("stdin exception!");
          throw new Error(e);
        }
      }
    }
    .start(); // Starts now
  }

  // Notify our writing thread that it should send more data to the process
  void write(String command) {
    try { 
      inputQueue.put(command);
    }
    catch( InterruptedException e ) {
      println("Interrupted Exception caught");
    }
  }


  boolean hasData() {
    return (outputQueue.size() > 0);
  }

  String read() {
    return (String) outputQueue.poll();
  }
}

