using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
//using Naudio.Wave;

//https://mark-dot-net.blogspot.com/2009/10/playback-of-sine-wave-in-naudio.html
namespace KinectApp
{
    internal class SoundProvider : WaveProvider32
    {
        int sample;
        public float Frequency { get; set; }
        public float Volume { get; set; }
        
        public SoundProvider() {
            Frequency = 1000;
            Volume = 0.25f;

        }

        //computes values of samples asked by the sound chip 
        public override int Read(byte[] buffer, int offset, int count)
        {
            int sampleRate = WaveFormat.SampleRate;
            for (int i = 0;  i < count; i++) {
                //y(t) = A⋅sin(2πft)(added in the buffer)
                buffer(offset + i) = (float)Volume*Math.Sin(2*Math.PI*Frequency*)
        }

    }
}
