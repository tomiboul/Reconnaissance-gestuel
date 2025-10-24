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
    private string statusText = null;
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
            this.kinectSensor.IsAvailableChanged += this.Sensor_IsAvailableChanged;

            // on ouvre le capteur - demarrage de tous les flux de donn�es
            kinectSensor.Open();
            this.StatusText = this.kinectSensor.IsAvailable ? Properties.Resources.RunningStatusText
                                                            : Properties.Resources.NoSensorStatusText;
            Console.WriteLine("La kinect est d�tect�e");
            Console.WriteLine("Ouverture du capteur");
            
            // on d�marre la lecture de la frame
            //readBodyframe();
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


    private void Sensor_IsAvailableChanged(object sender, IsAvailableChangedEventArgs e)
    {
        // on failure, set the status text
        this.StatusText = this.kinectSensor.IsAvailable ? Properties.Resources.RunningStatusText
                                                        : Properties.Resources.SensorNotAvailableStatusText;
    }
        
    static void Main(string[] args)
    {
        Console.WriteLine("Coucou");

        // on cr�e une instance de la class
        Liaison_Kinect liaisonKinect = new Liaison_Kinect();
        liaisonKinect.initKinect();
    }
}