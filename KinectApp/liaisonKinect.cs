using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Reflection;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Microsoft.Kinect;

 // dans le terminal -> etre via 'cd' dans le fichier -> executer "   dotnet run  "
 // source : initKinect/MainWindow.xaml.cs

class liaisonKinect
{

    private KinectSensor kinectSensor = null;
    private BodyFrameReader bodyFrameReader;
    private Body[] bodies = null;
    private string statusText = null;


    /*
    Initialisation de la kinect 
    */
    public void initKinect()
    {
        kinectSensor = kinectSensor.GetDefault();
        if (kinectSensor == null)
        {
            Console.WriteLine("La kinect n'est pas détectée");
            break;
        }
        else
        {
            Console.WriteLine("La kinect est détectée");
            // on ouvre le capteur
            kinectSensor.Open();
            this.InitializeComponent();
        }
    }

    /*
    Lecture des données du kinect
    */
    public void readBodyframe()
    {
        bodyFrameReader = kinectSensor.BodyFrameSource.OpenReader();
        // ...
    }


    static void Main(string[] args)
    {
        Console.WriteLine("coucou");

        // on crée une instance de la class
        liaisonKinect liaisonKinect = new liaisonKinect();
        liaisonKinect.initKinect();


    }
}