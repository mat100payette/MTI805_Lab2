using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Emgu.CV;
using Emgu.CV.UI;
using Emgu.CV.Structure;
using Emgu.CV.Util;
using Emgu.CV.Stitching;

namespace Emgu_Panorama
{
    public partial class frmMain : Form
    {
        Mat result = new Mat();
        Stitcher stitcher = new Stitcher(false);
        Mat image1 = new Mat("C:/Users/agosselin/Desktop/MTI805_Lab2/Boat/boat1.jpg");
        Mat image2 = new Mat("C:/Users/agosselin/Desktop/MTI805_Lab2/Boat/boat2.jpg");
        Mat image3 = new Mat("C:/Users/agosselin/Desktop/MTI805_Lab2/Boat/boat3.jpg");
        Mat image4 = new Mat("C:/Users/agosselin/Desktop/MTI805_Lab2/Boat/boat4.jpg");
        public frmMain()
        {
            InitializeComponent();
            VectorOfMat vmImage = new VectorOfMat(image1, image2, image3, image4);
            stitcher.Stitch(vmImage, result);

            ImageViewer.Show(result);
        }

    }
}
