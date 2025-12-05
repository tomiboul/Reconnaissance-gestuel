// Importing the required Librairies
using System;
using System.Data;
using System.Linq;
using Microsoft.Kinect;
using KinectApp;
using NAudio.Wave;
using System.Windows.Controls;

//https://codebeautify.org/csharpviewer#

namespace KinectHeadPositionConsole
{
    // Main class of the Program
    class Program
    {

        //Kinect related variable 
        private static KinectSensor sensor = null;
        private static Body[] bodies = null;
        private static BodyFrameReader bodyFrameReader = null;

        //Sinewave related variable 
        private static WaveOut waveOut = null;
        private static SoundProvider soundProvider;
        private static int frame = 0;
        private static DateTime lastFrame = DateTime.Now;

        //framerate of the kinect device, frequency and volume used for pitch interpolation
        const int max_frequency = 600;
        const int min_frequency = 20;
        const int frameRate = 30;
        private static float lastFreq;
        private static float currentFreq;
        private static float lastVol;
        private static float currentVol;
        private static float previous_distance;

        private static int loopFrame;
        private static bool active;
        private static int frameSinceActivation;
        private static CameraSpacePoint prev_position_hand_right;

        static void Main(string[] args)
        {

            //Initializes the sensor and the frame reader
            sensor = KinectSensor.GetDefault();
            sensor.Open();

            bodyFrameReader = sensor.BodyFrameSource.OpenReader();
            bodyFrameReader.FrameArrived += BodyFrameReader_FrameArrived;

            //Main loop to execute the program, escape to quit 
            while (true)
            {
                if (Console.KeyAvailable && Console.ReadKey(true).Key == ConsoleKey.Escape)
                    break;

                //increment to keep track of the frames since the activation (to deactivate it after some time)
                if (active)
                {
                    frameSinceActivation++;
                }
                loopFrame++;
                System.Threading.Thread.Sleep(50);
            }

            //Frees the resources
            bodyFrameReader.FrameArrived -= BodyFrameReader_FrameArrived;
            bodyFrameReader.Dispose();
            sensor.Close();
            StopSineWave();

            Console.WriteLine("Stopped");
        }

        //function that is executed each time a frame arrive 
        private static void BodyFrameReader_FrameArrived(object sender, BodyFrameArrivedEventArgs e)
        {
            using (BodyFrame f = e.FrameReference.AcquireFrame()) //gets the current frame 
            {
               
                frame++;

                if (f != null)
                {
                    if (bodies == null)
                    {
                        bodies = new Body[f.BodyCount];
                    }
                    else
                    {

                        f.GetAndRefreshBodyData(bodies);

                        //init the soundprovider instance
                        if (waveOut == null)
                        {
                            StartSineWave();
                        }

                        //gets the body tracked by the kinect device
                        Body trackedBody = null;
                        for (int i = 0; i < bodies.Length; i++)
                        {
                            if (bodies[i] != null && bodies[i].IsTracked)
                            {
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
                            Joint head = trackedBody.Joints[JointType.Head];
                            CameraSpacePoint position_head = head.Position;

                            float hands_distance = utility.compute_distance(position_hand_right.X, position_hand_right.Y, position_hand_left.X, position_hand_left.Y);
                            float right_hand_x_head_distance = utility.compute_distance(position_hand_right.X, position_hand_right.Y, position_head.X, position_head.Y);
                            float left_hand_x_head_distance = utility.compute_distance(position_hand_left.X, position_hand_left.Y, position_head.X, position_head.Y);

                            lastFreq = currentFreq;
                            lastVol = currentVol;
                            //can be changed if leads to bad audios




                            //currentVol = (float)(Math.Cos(6*distance+Math.PI)+1)/2;
                            currentVol = 0.4f;
                            currentFreq = 200 / hands_distance;


                            if (prev_position_hand_right.Z<=0) {
                            prev_position_hand_right = position_hand_right;
                            }
                        
                            if (!(active))
                            {
                                active = DetectActivationGesture(prev_position_hand_right, position_hand_right);
                            }
                            else
                            {
                                if (frameSinceActivation >= 90)
                                {
                                    Console.WriteLine("###############\nDeactivation after 90 frames\n###############");
                                    frameSinceActivation = 0;
                                    active = false;
                                    currentVol = 0;
                                    UpdateSineWave(currentVol, currentFreq);
                                }
                            }
                                prev_position_hand_right = position_hand_right;


                            //if hands too far away from head, do not consider it 
                            if (active)
                            {
                                if (right_hand_x_head_distance <= 0.7 && left_hand_x_head_distance <= 0.7)
                                {
                                    //if distance between hands does not change, do not consider it

                                    if (Math.Abs(previous_distance - hands_distance) <= 0.01)
                                    {
                                        Console.WriteLine(lastVol);
                                        //if (lastVol <= 0.2f)
                                        //{
                                        if (lastVol <= 0.05f)
                                        {
                                            currentVol = 0;
                                        }
                                        else
                                        {
                                            currentVol = lastVol / 1.2f;
                                        }
                                        //}
                                        //else
                                        //{
                                        //   currentVol = 0.2f;
                                        //}
                                    }


                                    previous_distance = hands_distance;


                                    //bounds the frequency between constants min_frequency and max_frequency
                                    if (currentFreq <= min_frequency)
                                    {
                                        currentFreq = min_frequency;
                                    }
                                    if (currentFreq >= max_frequency)
                                    {
                                        currentFreq = max_frequency;
                                    }
                                }
                                else
                                {
                                    currentVol = 0;
                                }



                                UpdateSineWave(currentVol, currentFreq);
                            }
                            //else
                            //{
                                //currentVol = 0;
                                //UpdateSineWave(currentVol, currentFreq);
                            //}
                            //Console.WriteLine(distance);

                        }
                    }
                }
                lastFrame = DateTime.Now;
                //Console.WriteLine("frame finsihed");
            }
        }

        // Initialize the Sinewave 
        private static void StartSineWave()
        {
            if (waveOut == null)
            {

                soundProvider = new SoundProvider();
                soundProvider.SetWaveFormat(16000, 1); // 16kHz mono
                soundProvider.Frequency = 500;
                soundProvider.Volume = 0.2f;
                
                lastFreq = 1000;
                lastVol = (float)0.4;
                waveOut = new WaveOut();
                waveOut.DesiredLatency = 120;
                waveOut.Init(soundProvider);
                waveOut.Play();
            }
        }

        // Stop the Sinewave
        private static void StopSineWave()
        {
            if (!(waveOut == null))
            {
                waveOut.Stop();
                waveOut.Dispose();
                waveOut = null;
            }
        }

        // Update Sinewave state
        private static void UpdateSineWave(float Vol, float Freq)
        {
            if (!(soundProvider == null))
            {
                soundProvider.targetFreq = Freq;
                soundProvider.targetVol = Vol;
            }
        }


        private static bool DetectActivationGesture(CameraSpacePoint previous_position_hand_right, CameraSpacePoint position_hand_right)
        {
            
            if (previous_position_hand_right.X - position_hand_right.X>0.06/Math.Sqrt(position_hand_right.Z))
            {
                Console.WriteLine("###############\ndetected gesture\n###############");
                return true;
                
            }
            return false;
        }
    }
}