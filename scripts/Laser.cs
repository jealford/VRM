/* SceneHandler.cs*/

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using Valve.VR.Extras;

public class Laser : MonoBehaviour
{
    private GameObject selected;
    private GameObject oldSelected;
    public SteamVR_LaserPointer laserPointer;
    public Material picked;
    public Material forgotten;

    public GameObject[] types;
    public GameObject[] rotators;
    private DataGetter _dataGetter;

    void Awake()
    {
        laserPointer.PointerIn += PointerInside;
        laserPointer.PointerOut += PointerOutside;
        laserPointer.PointerClick += PointerClick;
    }

    void Start()
    {
        _dataGetter = new DataGetter();
        // DataGetter.targetPosition = target.transform.position;
        _dataGetter.Start();

        /*ForceDotNet.Force();
        client = new RequestSocket();
        client.Connect("tcp://*:5555");*/
    }

    private int count = 0;

    public void PointerClick(object sender, PointerEventArgs e)
    {
        if (e.target.name.Equals("next"))
        {
            count = ++count % 5;
            oldSelected = selected;
            selected = types[count];

            selected.GetComponent<Renderer>().material = picked;
            oldSelected.GetComponent<Renderer>().material = forgotten;
        }
        else if (e.target.name.Equals("go"))
        {
            selected.GetComponent<Renderer>().material = forgotten;
            selected = null;
            Debug.Log("Ready to GO");

            DataGetter.angles = new[]
            {
                rotators[0].transform.rotation.y, rotators[1].transform.rotation.x, rotators[2].transform.rotation.x,
                rotators[3].transform.rotation.x
            };
            DataGetter.isReady = true;
        }
    }

    public void PointerInside(object sender, PointerEventArgs e)
    {
    }

    public void PointerOutside(object sender, PointerEventArgs e)
    {
    }

    public void Update()
    {
        if (selected && (count >= 0 && count < 3))
        {
            var angle = selected.transform.parent.transform.rotation.eulerAngles;
            angle.x = laserPointer.gameObject.transform.localRotation.eulerAngles.z;
            selected.transform.parent.transform.eulerAngles = angle;
        }
        else if (selected)
        {
            var angle = selected.transform.parent.transform.rotation.eulerAngles;
            angle.y = laserPointer.gameObject.transform.localRotation.eulerAngles.z;
            selected.transform.parent.transform.eulerAngles = angle;
        }
    }

    private void OnDestroy()
    {
        _dataGetter.Stop();
    }
}