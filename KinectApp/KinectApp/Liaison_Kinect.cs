using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Reflection;
using System.Windows;
using Microsoft.Kinect;

 // dans le terminal -> etre via 'cd' dans le fichier -> executer "   dotnet run  "
 // source : initKinect/MainWindow.xaml.cs

class Liaison_Kinect
{

    private KinectSensor kinectSensor = null;
    private BodyFrameReader bodyFrameReader;
    private Body[] bodies = null;


    /*
        Initialisation de la kinect 
    */
    public void initKinect()
    {
        kinectSensor = KinectSensor.GetDefault();
        if (kinectSensor == null)
        {
            Console.WriteLine("La kinect n'est pas d�tect�e");
        }
        else
        {
            Console.WriteLine("La kinect est d�tect�e");
            // on ouvre le capteur
            kinectSensor.Open();

            // on d�marre la lecture de la frame
            // readBodyframe();
        }
    }

    /*
        Cloture de la kinect
    */
    public void closeKinect(){
        if(kinectSensor != null){
            kinectSensor = null;
            Console.WriteLine("La kinect vient de se d�connect�e");
        }
    }



    /*
        Lecture des donn�es du kinect
    */
    public void readBodyframe()
    {
        bodyFrameReader = kinectSensor.BodyFrameSource.OpenReader();
        // ...
    }
    

    static void Main(string[] args)
    {
        Console.WriteLine("coucou");

        // on cr�e une instance de la class
        // LiaisonKinect liaisonKinect = new LiaisonKinect();
        // liaisonKinect.initKinect();

        initKinect();


    }
}