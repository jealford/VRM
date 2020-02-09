using System;
using System.Collections;
using System.Collections.Generic;
using AsyncIO;
using UnityEngine;
using NetMQ;
using NetMQ.Sockets;


public class JointSet : MonoBehaviour
{
    private DataGetter _dataGetter;
    
    private Vector3 prevTargetPosition;
    
    public GameObject target;
    
    //private RequestSocket client;
    // Start is called before the first frame update
    void Start()
    {
        _dataGetter = new DataGetter();
       // DataGetter.targetPosition = target.transform.position;
        _dataGetter.Start();
        
        /*ForceDotNet.Force();
        client = new RequestSocket();
        client.Connect("tcp://*:5555");*/
    }

    /*
    string makeGoalJSON(GameObject target)
    {
        var position = target.transform.position;
        return "{\"goal_position\":[" + position.x/3 + "," + position.z/3 + "," +
               position.y/3 + "]}";
    }
    */
    
    // Update is called once per frame

    
    
    void Update()
    {
        /*DataGetter.targetPosition = target.transform.position;

        if (target.transform.position != prevTargetPosition)
        {
            prevTargetPosition = target.transform.position
            double[] angles = DataGetter.angles;
            var obj = gameObject;
            var angle = obj.transform.localRotation.eulerAngles;
            angle.z = (float) angles[4];
            obj.transform.localRotation = Quaternion.Euler(angle);
            for (var i = 3; i > 0; i--)
            {
                obj = obj.transform.parent.gameObject;
                angle = obj.transform.localRotation.eulerAngles;
                angle.x = (float) angles[i];
                obj.transform.localRotation = Quaternion.Euler(angle);
            }

            obj = obj.transform.parent.gameObject;
            angle = obj.transform.localRotation.eulerAngles;
            angle.y = (float) angles[0];
            obj.transform.localRotation = Quaternion.Euler(angle);
        }*/
    }

    private void OnDestroy()
    {
        _dataGetter.Stop();
    }
}