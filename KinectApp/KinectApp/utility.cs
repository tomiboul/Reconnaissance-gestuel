using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace KinectApp
{
    public static class utility
    {
        public static float compute_distance(float X_1, float Y_1, float X_2, float Y_2)
        {
            return (float)Math.Sqrt(Math.Pow(Convert.ToDouble(X_2 - X_1), Convert.ToDouble(2))+Math.Pow(Convert.ToDouble(Y_2-Y_1), Convert.ToDouble(2)));
        }
    }
}
