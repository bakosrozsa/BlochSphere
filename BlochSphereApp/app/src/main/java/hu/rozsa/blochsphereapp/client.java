package hu.rozsa.blochsphereapp;

import android.os.AsyncTask;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class client extends AsyncTask<String,Void,Void> {
    Socket socket;
    private Exception exc;
    @Override
    protected Void doInBackground(String... params) {
        try {
            socket = new Socket("192.168.0.108",8888);
        }
        catch (Exception e){
            this.exc = e;
            return null;
        }
        return null;
    }
    public void kuld(String x){
        try{
            PrintWriter outToServer = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
            outToServer.print(x);
            outToServer.flush();
        }
        catch (IOException e){
            e.printStackTrace();
        }
    }
}
