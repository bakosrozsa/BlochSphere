package hu.rozsa.blochsphereapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;

public class MainActivity extends AppCompatActivity implements SensorEventListener{

    private SensorManager sensorManager;
    private Sensor sensor;
    private boolean clicked;
    Socket socket;
    PrintWriter outToServer;
    String angles;
    String[] gates = new String[]{"Home","Identity","Pauli-x","Pauli-y","Pauli-z","Hadamard","Phase","T"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button connection_button = (Button) findViewById(R.id.button);
        EditText ip_port = (EditText) findViewById(R.id.editTextText);
        Spinner gates_spinner = findViewById(R.id.spinner);
        TextView info_textView = findViewById(R.id.textView2);
        ImageView gate_imageView = findViewById(R.id.imageView);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1,gates);
        gates_spinner.setAdapter(adapter);

        clicked = false;
        int SDK_INT = android.os.Build.VERSION.SDK_INT;
        if (SDK_INT > 8)
        {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder()
                    .permitAll().build();
            StrictMode.setThreadPolicy(policy);
            connection_button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (!clicked)
                    {
                        clicked = true;
                        String[] connectiondata = ip_port.getText().toString().split(":");
                        try {
                            socket = new Socket();
                            socket.connect(new InetSocketAddress(connectiondata[0],Integer.parseInt(connectiondata[1])),100);
                            outToServer = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
                        }
                        catch (IOException e) {
                            Toast.makeText(MainActivity.this, "Check your connections!",
                                    Toast.LENGTH_LONG).show();
                            clicked = false;
                            return;
                        }
                        catch (ArrayIndexOutOfBoundsException | IllegalArgumentException e){
                            Toast.makeText(MainActivity.this, "Wrong address!",
                                    Toast.LENGTH_LONG).show();
                            clicked = false;
                            return;
                        }
                        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
                        sensor = sensorManager.getDefaultSensor(Sensor.TYPE_ORIENTATION);
                        sensorManager.registerListener(MainActivity.this,sensor,SensorManager.SENSOR_DELAY_NORMAL);
                        ip_port.getText().clear();
                        ip_port.setEnabled(false);
                        Toast.makeText(MainActivity.this, "Phone connected!",
                                Toast.LENGTH_LONG).show();
                    }
                    else
                    {
                        clicked = false;
                        outToServer.flush();
                        sensorManager.unregisterListener(MainActivity.this);
                        try {
                            socket.close();
                        } catch (IOException e) {
                            Toast.makeText(MainActivity.this, "Can't disconnect! Check your connections and try again!",
                                    Toast.LENGTH_LONG).show();
                        }
                        ip_port.setEnabled(true);
                    }
                }
            });
            gates_spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
                @Override
                public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                    switch (gates[position]){
                        case "Home":
                            info_textView.setText(String.format("In quantum computing and specifically the quantum circuit " +
                                    "model of computation,a quantum logic gate (or simply quantum gate) is a basic quantum" +
                                    " circuit operating on a small number of qubits. Quantum logic gates are the building blocks of quantum circuits," +
                                    " like classical logic gates are for conventional digital circuits." +
                                    "\n\n\nThis app is for a quantum logic gates teaching program, to help the students learn " +
                                    "them more easily, by interacting with the bloch sphere, by rotating the vector and " +
                                    "using gates on it. Keep in mind, that there are several other quantum logic gates,  but these are the most common ones that are using one qubit."));
                            gate_imageView.setVisibility(view.INVISIBLE);
                            break;
                        case "Identity":
                            info_textView.setText(String.format("The Identity gate is a single-qubit operation that leaves the basis states |0> and |1> unchanged."));
                            gate_imageView.setVisibility(view.VISIBLE);
                            gate_imageView.setImageResource(R.drawable.identity);
                            break;
                        case "Pauli-x":
                            info_textView.setText(String.format("This gate is analogous to the NOT gate in classical computing. It flips the state of the qubit from |0⟩ to |1⟩ or from |1⟩ to |0⟩."));
                            gate_imageView.setVisibility(view.VISIBLE);
                            gate_imageView.setImageResource(R.drawable.paulix);
                            break;
                        case "Pauli-y":
                            info_textView.setText(String.format("This gate is equivalent to applying both X and Z gates and a global phase."));
                            gate_imageView.setVisibility(view.VISIBLE);
                            gate_imageView.setImageResource(R.drawable.pauliy);
                            break;
                        case "Pauli-z":
                            info_textView.setText(String.format("This gate flips the phase of the |1⟩ state, leaving the |0⟩ state unchanged."));
                            gate_imageView.setVisibility(view.VISIBLE);
                            gate_imageView.setImageResource(R.drawable.pauliz);
                            break;
                        case "Hadamard":
                            info_textView.setText(String.format("This gate creates a superposition state by transforming the |0⟩ state into an equal superposition of the |0⟩ and |1⟩ states."));
                            gate_imageView.setVisibility(view.VISIBLE);
                            gate_imageView.setImageResource(R.drawable.hadamard);
                            break;
                        case "Phase":
                            info_textView.setText(String.format("The S gate is also known as the phase gate or the Z90 gate, because it represents a 90-degree rotation around the z-axis."));
                            gate_imageView.setVisibility(view.VISIBLE);
                            gate_imageView.setImageResource(R.drawable.phase);
                            break;
                        case "T":
                            info_textView.setText(String.format("It induces a π/4 phase, and is " +
                                    "sometimes called the pi/8 gate"));
                            gate_imageView.setVisibility(view.VISIBLE);
                            gate_imageView.setImageResource(R.drawable.tgate);
                            break;
                    }
                }

                @Override
                public void onNothingSelected(AdapterView<?> parent) {

                }
            });
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        angles =  event.values[0] + "," +
                event.values[2] * 2;
        outToServer.print(angles);
        outToServer.flush();
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }
}