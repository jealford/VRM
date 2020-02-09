using System.Collections;
using System.Collections.Generic;
using AsyncIO;
using UnityEngine;
using NetMQ;
using NetMQ.Sockets;
using UnityEditor;

public class DataGetter : RunAbleThread
{
    struct Packet
    {
        public float temperature;
        public float moisture;
    }

    public static float[] angles { get; set; }

    public static bool isReady = false;

    string makeAngleJSON()
    {
        return "{\"motor_angles\":[" + angles[0] + "," + angles[1] + "," +
               angles[2]+ "," + angles[3] + "]}";
    }
    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
            client.Connect("tcp://localhost:5555");

            while(Running)
            {
                Debug.Log("Request");
                if (isReady)
                {
                    client.SendFrame(makeAngleJSON());
                    string message = null;
                    bool gotMessage = false;
                    while (Running)
                    {
                        gotMessage = client.TryReceiveFrameString(out message); // this returns true if it's successful
                        if (gotMessage) break;
                    }
                    if (gotMessage)
                    {
                        Debug.Log("Received " + message);
                        isReady = false;
                    }

                }
            }
        }

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}