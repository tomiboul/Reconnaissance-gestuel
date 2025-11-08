using System;
using System.Data;
using System.Linq;
using Microsoft.Kinect;
using KinectApp;
using NAudio.Wave;
using System.Windows.Controls;

namespace KinectHeadPositionConsole
{
    class Program
    {
        private static float treshold;
        private static KinectSensor sensor = null;
        private static Body[] bodies = null;
        private static BodyFrameReader bodyFrameReader = null;
        private static WaveOut waveOut = null;
        private static SoundProvider soundProvider;
        private static int frame = 0;
        private static DateTime lastFrame = DateTime.Now;

        //framerate of the kinect device, frequency and volume used for pitch interpolation
        private const int frameRate = 30;
        private static float lastFreq;
        private static float currentFreq;
        private static float lastVol;
        private static float currentVol;
        private static float previous_distance;

        private static float loopFrame;

        static void Main(string[] args)
        {
                
                //initializes the sensor aand the frame reader
                sensor = KinectSensor.GetDefault();

                sensor.Open();


                bodyFrameReader = sensor.BodyFrameSource.OpenReader();

                bodyFrameReader.FrameArrived += BodyFrameReader_FrameArrived;

                //main loop to execute the program, escape to quit 
                while (true)
                {
                    if (Console.KeyAvailable && Console.ReadKey(true).Key == ConsoleKey.Escape)
                        break;

                
                    loopFrame++;

                    System.Threading.Thread.Sleep(50);
                }


                //frees the resources

                bodyFrameReader.FrameArrived -= BodyFrameReader_FrameArrived;
                bodyFrameReader.Dispose();
                sensor.Close();
                StopSineWave();
               

                Console.WriteLine("Stopped");


            
        }

        private static void BodyFrameReader_FrameArrived(object sender, BodyFrameArrivedEventArgs e)
        {
            using (BodyFrame f = e.FrameReference.AcquireFrame())//gets the current frame 
            {
                //Console.WriteLine("frame count : " + frame);
                frame++;
                
                if (f != null)
                {
                    if (bodies == null)
                    {
                        bodies = new Body[f.BodyCount];
                    }
                    else {

                        f.GetAndRefreshBodyData(bodies);

                        //init the soundprovider instance
                        
                        if (waveOut == null)
                        {
                            StartSineWave();   
                        }

                        //gets the body tracked by the kinect device
                        Body trackedBody = null;
                        for (int i = 0; i < bodies.Length; i++) {
                            if (bodies[i] != null && bodies[i].IsTracked) { 
                                trackedBody = bodies[i];
                            }
                        }

                        //gets the actual joints of the tracked body
                        if (trackedBody != null)
                        {
                            Joint right_hand_j = trackedBody.Joints[JointType.HandRight];
                            CameraSpacePoint position_hand_right = right_hand_j.Position;
                            Joint left_hand_j = trackedBody.Joints[JointType.HandLeft];
                            CameraSpacePoint position_hand_left = left_hand_j.Position;
                            
                            float distance = utility.compute_distance(position_hand_right.X, position_hand_right.Y, position_hand_left.X, position_hand_left.Y);


                            lastFreq = currentFreq;
                            lastVol = currentVol;
                            //can be changed if leads to bad audios

                            //currentVol = (float)(Math.Cos(6*distance+Math.PI)+1)/2;
                            currentVol = 0.4f;
                            currentFreq = 300 / distance;
                            
                            
                            if (Math.Abs(previous_distance - distance) <= 0.01)
                            {
                                currentVol = 0;
                            }
                            previous_distance = distance;

                            if (currentFreq <= 20) {
                                currentFreq = 20;
                            }
                            if (currentFreq >= 800) {
                                currentFreq = 800;
                            }


                            //Console.WriteLine("updated normally");
                            UpdateSineWave(currentVol, currentFreq);
                            
                            //Console.WriteLine(distance);
                         
                        }                                              
                    }
                }
                lastFrame = DateTime.Now;
                //Console.WriteLine("frame finsihed");
            }
        }

        private static void StartSineWave()
        {
            if (waveOut == null)
            {
            
                soundProvider = new SoundProvider();
                soundProvider.SetWaveFormat(16000, 1); // 16kHz mono
                soundProvider.Frequency = 500;
                soundProvider.Volume = 0;
                lastFreq = 1000;
                lastVol = (float)0.4;
                waveOut = new WaveOut();
                waveOut.DesiredLatency = 120;
                waveOut.Init(soundProvider);
                waveOut.Play();
            }
        }

        private static void StopSineWave() {
            if (!( waveOut == null))
            {
                waveOut.Stop();
                waveOut.Dispose();
                waveOut = null;
            }
        }

        private static void UpdateSineWave(float Vol, float Freq)
        {
            if (!(soundProvider == null))
            {
                soundProvider.targetFreq = Freq;
                soundProvider.targetVol = Vol;
            }
        }
    }
}