using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Net.Mail;
using System.Configuration;
using System.Data.SqlClient;
using System.Text.RegularExpressions;


namespace H2_Debug___STUDENT
{
    public partial class HOME : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {

        }

        protected void btnTextInBox_Click(object sender, EventArgs e)
        {
            //This button will make the image instructions visible and
            //the Pistol Pete image visible with a corresponding button.
            lblImageMessage.Visible = true;
            imgPistolPete.Visible = true;
            btnImageDisplayed.Visible = true;
        }

        protected void btnImageDisplayed_Click(object sender, EventArgs e)
        {
            //Check if the image is correct.
            string matchString = imgPistolPete.ImageUrl.ToString();
            if (matchString == "~/images/PistolPeteCC.jpg")
            {
                //This code will display the shortname prompt label, textbox and validator.
                lblShortNameLabel.Visible = true;
                tboxShortName.Visible = true;
                rfvShortName.Visible = false;

                //Please the cursor in the visible ShortName textbox.
                tboxShortName.Focus();

                //Hide the error message text;
                lblImgErrMsg.Text = "";
                lblImgErrMsg.Visible = false;
            }
            else
            {
                lblImgErrMsg.Text = "Please make the image display above before continuing.";
                lblImgErrMsg.Visible = true;
            }
        }

        protected void tboxShortName_TextChanged(object sender, EventArgs e)
        {
            //If all validation passes, make the code button appear.
            if (IsValid)
            {
                btnGetCode.Visible = true;
            }
        }

        protected void btnGetCode_Click(object sender, EventArgs e)
        {
            //This should be a comment. Make it a comment to avoid the compiler errors.

            //This will read the database to get a unique code just for you.
            SqlConnection MyConnection = new SqlConnection(ConfigurationManager.ConnectionStrings["zz_kstromConnectionString"].ConnectionString);

            string sqlQuery = "SELECT * from H1_StudentCode WHERE StudentShortName = '" + tboxShortName.Text + "';";
            SqlCommand MyCommand = new SqlCommand(sqlQuery, MyConnection);
            SqlDataReader MyReader;

            //Set the message to an invalid message initially. It will be
            //overridden if a valid shortname is found in the database.
            lblMessage.Text = "Invalid Shortname entered. Please try again.";
            lblMessage.Visible = true;

            try
            {
                MyConnection.Open();

                MyReader = MyCommand.ExecuteReader();

                while (MyReader.Read())
                {
                    lblMyCode.Text = MyReader["StudentCode"].ToString();
                    string secretmessage = MyReader["SecretMessage"].ToString();
                    lblMyCode.Visible = true;
                    lblCodeLabel.Visible = true;
                    btnEmailCode.Visible = true;
                    lblMessage.Visible = true;
                    lblMessage.Text = "Congratlations! Please continue!";
                    lblMyEmailLabel.Visible = true;
                    tboxEmail.Visible = true;
                    lblMyPasswordLabel.Visible = true;
                    tboxPassword.Visible = true;
                }
            }
            catch (Exception)
            {
                lblMessage.Text = "Invalid Shortname entered. Please try again.";
            }
            finally
            {
                MyConnection.Close();
            }
        }

        protected void btnEmailCode_Click(object sender, EventArgs e)
        {
            //This code will email your code to Professor Strom.
            //You will still need to screen shot your final page and
            //submit to the dropbox.
            try
            {
                String userName = tboxEmail.Text;
                String password = tboxPassword.Text;
                MailMessage msg = new MailMessage();
                msg.To.Add(new MailAddress("kim.strom@okstate.edu"));
                msg.From = new MailAddress(userName);
                msg.Subject = "Homework #1 Code";
                msg.Body = "My code for Homework #1 is: " + lblMyCode.Text;
                msg.IsBodyHtml = true;
                SmtpClient client = new SmtpClient();
                client.Host = "smtp.office365.com";
                client.Credentials = new System.Net.NetworkCredential(userName, password);
                client.Port = 587;
                client.EnableSsl = true;
                client.Send(msg);

                lblSuccess.Text = "Your code has been sent to Professor Strom. Print this page to a pdf and upload the pdf to Canvas.";
            }
            catch (Exception)
            {
                lblSuccess.Text = "Email credentials are invalid. Please try again.";
            }
        }
    }
}
