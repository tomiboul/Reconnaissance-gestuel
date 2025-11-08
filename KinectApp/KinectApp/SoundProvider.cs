using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NAudio.Wave;

//https://mark-dot-net.blogspot.com/2009/10/playback-of-sine-wave-in-naudio.html
namespace KinectApp
{
    internal class SoundProvider : WaveProvider32
    {
        int sample;
        public float Frequency { get; set; }
        public float Volume { get; set; }

        private double phase;

        //variables to modify the sound in a fluid way
        public float targetFreq;    
        public float targetVol;
        private float coeffFreq = 0.03f;
        private float coeffVol = 0.03f;
        public SoundProvider() {
            Frequency = 1000;
            Volume = 0.25f;
            phase = 0;

        }

        //computes values of samples asked by the sound chip 
        public override int Read(float[] buffer, int offset, int count)
        {
           
            double phasediff = 2 * Math.PI * Frequency / WaveFormat.SampleRate;

            //target frequency and volumes to modify the sound in a fluid way, and if the frequency greatly differs from one frame to another, the sound changes faster
            coeffFreq = Math.Max(0.03f, Math.Abs(targetFreq- Frequency)*0.0005f);
            Frequency += (targetFreq - Frequency) * coeffFreq;
            coeffFreq = Math.Max(0.03f, Math.Abs(targetVol - Volume));
            
            Volume += (targetVol - Volume) * coeffVol;
            Console.WriteLine("Changement");
            Console.WriteLine(targetVol);
            Console.WriteLine(Volume);
            if (Volume<= 0.1&& targetVol == 0) { Volume = 0; }
            if (Volume <= 0.1 && targetVol != 0) { Volume += 0.1f; }
            for (int i = 0; i < count; i++)
            {
                //y(t) = A⋅sin(2πft)(added in the buffer)
                buffer[offset+i] = (float)(Volume * Math.Sin(phase));
                phase += phasediff;
                if (phase > 2 * Math.PI) 
                {
                    phase -= 2 * Math.PI; 
                }
            }
            return count;
        }
    }
}
