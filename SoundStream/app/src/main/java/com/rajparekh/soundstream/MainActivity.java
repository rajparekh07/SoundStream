package com.rajparekh.soundstream;

import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.koushikdutta.async.AsyncServer;
import com.koushikdutta.async.ByteBufferList;
import com.koushikdutta.async.DataEmitter;
import com.koushikdutta.async.callback.DataCallback;
import com.koushikdutta.async.http.AsyncHttpClient;
import com.koushikdutta.async.http.WebSocket;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.drafts.Draft;
import org.java_websocket.handshake.ServerHandshake;

import java.net.URI;
import java.util.zip.DataFormatException;
import java.util.zip.Inflater;

public class MainActivity extends AppCompatActivity {

    private Button mConnectButton;

    private Button mStopButton;

    private WebSocket mSocket;

    private EditText mIPText;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        mIPText = (EditText) findViewById(R.id.editText);
        mConnectButton = (Button) findViewById(R.id.connect);

        mConnectButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                connect();
                Toast.makeText(MainActivity.this, "Hi", Toast.LENGTH_SHORT).show();
            }
        });

        mStopButton = (Button) findViewById(R.id.disconnect);

        mStopButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                disconnect();
            }
        });

    }

    AudioTrack mAudioTrack = new AudioTrack(AudioManager.STREAM_MUSIC, 22000, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT, AudioTrack.getMinBufferSize(22000, AudioFormat.CHANNEL_OUT_MONO, AudioFormat.ENCODING_PCM_16BIT), AudioTrack.MODE_STREAM);


    void connect() {
//        EmptyClient a = new EmptyClient(URI.create("ws://" + mIPText.getText().toString() + ":8000/"));
//        a.connect();

       AsyncHttpClient.getDefaultInstance().websocket("ws://" + mIPText.getText().toString() + ":8000/", "ws", new AsyncHttpClient.WebSocketConnectCallback() {
            @Override
            public void onCompleted(Exception ex, WebSocket webSocket) {
                if (ex != null) {
                    ex.printStackTrace();
                    return;
                }
                mSocket = webSocket;
                webSocket.setStringCallback(new WebSocket.StringCallback() {
                    public void onStringAvailable(String s) {
                        System.out.println("I got a string: " + s);
                    }
                });
                webSocket.setDataCallback(new DataCallback() {
                    public void onDataAvailable(DataEmitter emitter, ByteBufferList byteBufferList) {
                        // note that this data has been read
//                        byteBufferList.recycle();
//                        int bufferSize = AudioTrack.getMinBufferSize(44100, AudioFormat.CHANNEL_OUT_DEFAULT, AudioFormat.ENCODING_PCM_16BIT);
//                        System.out.println(byteBufferList.);
                        byte[] b = byteBufferList.getAllByteArray();
                        int bufferSize = b.length;

                        Inflater decompresser = new Inflater();
                        decompresser.setInput(b, 0, bufferSize);
                        byte[] result = new byte[bufferSize];
                        try {
                            bufferSize = decompresser.inflate(result);
                        } catch (DataFormatException e) {
                            e.printStackTrace();
                        }
                        decompresser.end();

                        mAudioTrack.write(result, 0, bufferSize);

                        mAudioTrack.play();

//                        audioRecordThread.start();

//                        mAudioTrack.release();
                    }
                });
            }
        });


    }

    void disconnect () {
        mSocket.send("INST:stop");
        mSocket.close();
    }
}

class EmptyClient extends WebSocketClient {
    public EmptyClient(URI serverUri, Draft draft) {
        super(serverUri, draft);
    }

    EmptyClient(URI serverURI) {
        super(serverURI);
        System.out.println(serverURI.toASCIIString());


    }

    @Override
    public void onOpen(ServerHandshake handshakedata) {
        System.out.println("new connection opened");
    }

    @Override
    public void onClose(int code, String reason, boolean remote) {
        System.out.println("closed with exit code " + code + " additional info: " + reason);
    }

    @Override
    public void onMessage(String message) {
        System.out.println("received message: " + message);
    }

    @Override
    public void onError(Exception ex) {
        System.err.println("an error occurred:" + ex);
    }
}