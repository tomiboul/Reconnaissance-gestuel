using System;
using System.Data;
using System.Linq;
using Microsoft.Kinect;
using KinectApp;

namespace KinectHeadPositionConsole
{
    class Program
    {
        private static float treshold 
        private static KinectSensor sensor = null;
        private static Body[] bodies = null;
        private static BodyFrameReader bodyFrameReader = null;

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

                    System.Threading.Thread.Sleep(50);
                }


                //frees the resources
                bodyFrameReader.FrameArrived -= BodyFrameReader_FrameArrived;
                bodyFrameReader.Dispose();
                sensor.Close();

                Console.WriteLine("Stopped");


            
        }

        private static void BodyFrameReader_FrameArrived(object sender, BodyFrameArrivedEventArgs e)
        {
            using (BodyFrame f = e.FrameReference.AcquireFrame())//gets the current frame 
            {
                if (f != null)
                {
                    if (bodies == null)
                    {
                        bodies = new Body[f.BodyCount];
                    }
                    else {

                            f.GetAndRefreshBodyData(bodies);

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
                            Console.WriteLine(distance);
                         
                        }                                              
                    }
                }
            }
        }
    }
}