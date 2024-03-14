package hu.rozsa.blochsphereapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity implements SensorEventListener{

    private SensorManager sensorManager;
    private Sensor sensor;
    private boolean clicked;
    Socket socket;
    PrintWriter outToServer;
    String angles;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button button = (Button) findViewById(R.id.button);
        Button button2 = (Button) findViewById(R.id.button2);

        clicked = false;
        int SDK_INT = android.os.Build.VERSION.SDK_INT;
        if (SDK_INT > 8)
        {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                    .permitAll().build();
            StrictMode.setThreadPolicy(policy);
            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (!clicked)
                    {
                        clicked = true;
                        try {
                            socket = new Socket("192.168.0.105",8888);
                            outToServer = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
                        }
                        catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    }
                    else
                    {
                        clicked = false;
                        outToServer.flush();
                        try {
                            socket.close();
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }
                    }
                }
            });
            button2.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
                    sensor = sensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION);
                    sensorManager.registerListener(MainActivity.this,sensor,SensorManager.SENSOR_DELAY_NORMAL);
                }
            });
        }

    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        angles = event.values[0] + "," +
                event.values[1];
        outToServer.print(angles);
        outToServer.flush();
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }
}