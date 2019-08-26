<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="HOME.aspx.cs" Inherits="H2_Debug___STUDENT.HOME" MaintainScrollPositionOnPostback="true" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>H2 DEBUG - HOME PAGE</title>
    <link href="https://fonts.googleapis.com/css?family=Cinzel&display=swap" rel="stylesheet" />
    <script src="Scripts/jquery-3.4.1.min.js"></script>
    <script src="Scripts/bootstrap.min.js"></script>
    <link href="Content/bootstrap.min.css" rel="stylesheet" />
    <link href="Content/H1Stylesheet.css" rel="stylesheet" />
</head>
<body>
    <form id="form1" runat="server">
        <div class="container">
            <div class="jumbotron">
                <h1>Welcome to Homework #1</h1>
            </div>
            <div class="row">
                <p>
                        Correct the HTML errors on this page that will enable 
                        this text to display inside the orange-bordered box.                
                    
                <div class="col-sm-12 orangebox">
                    </p>
                </div>
            <%--</div>--%> 
            <div class="row">
                <div class="col-sm-12 btnbox">
                    <asp:Button ID="btnTextInBox" runat="server" class="btn btn-dark" Text="CLICK once text is inside orange box." OnClick="btnTextInBox_Click" />
                </div>
            </div>
            <div class="row">
                <div id="ImageMessage" class="col-sm-6 imgmsgbox">
                    <asp:Label ID="lblImageMessage" runat="server" Text="Correct errors to make the image on the right display." Visible="False"></asp:Label>
                </div>
                <div id="PistolPete" class="col-sm-6">
                    <asp:Image ID="imgPistolPete" class="pistolpete d-block img-fluid mx-auto" runat="server" ImageUrl="~/imgaes/PistolPeteCC.jpg" Visible="False" /><br />
                    <br />
                    <asp:Button ID="btnImageDisplayed" runat="server" class="btn btn-dark d-block mx-auto" Text="CLIKC once image displays." Visible="False" OnClick="btnImageDisplayed_Click" />
                    <div class="LabelImgMsgText">
                        <asp:Label ID="lblImgErrMsg" runat="server" Text=""></asp:Label>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-4 ShortName">
                    <asp:Label ID="lblShortNameLabel" runat="server" Text="Enter yuor okstate Short Name: " Visible="False"></asp:Label>
                    <asp:TextBox ID="tboxShortName" runat="server" CssClass="form-control" Visible="False" AutoPostBack="True" CausesValidation="True" OnTextChanged="tboxShortName_TextChanged" ValidationGroup="ShortNameGroup"></asp:TextBox><br />
                    <asp:RequiredFieldValidator ID="rfvShortName" runat="server" ErrorMessage="Please enter your okstate Short Name." ControlToValidate="tboxShortName" ValidationGroup="ShortNameGroup"></asp:RequiredFieldValidator>
                </div>
                <div class="col-sm-4 ShortName ShortName2and3">
                    <asp:Button ID="btnGetCode" class="btn btn-dark btncodeassigned" runat="server" Text="CLICK to get your assigned code." Visible="False" OnClick="btnGetCode_Click" ValidationGroup="ShortNameGroup" />
                    <div>
                        <asp:Label ID="lblMessage" class="LabelCodeMsgText" runat="server" Visible="False"></asp:Label>
                    </div>
                </div>
                <div class="col-sm-4 ShortName ShortName2and3">
                    <asp:Label ID="lblCodeLabel" class="col-form-label" runat="server" Text="Your code is: " Visible="False"></asp:Label>
                    <asp:Label ID="lblMyCode" class="form-control" runat="server" Visible="False"></asp:Label>
                    <div class="LabelokstateText">
                        <asp:Label ID="lblMyEmailLabel" class="col-form-label" runat="server" Text="Enter your okstate email: " Visible="False"></asp:Label>
                        <asp:TextBox ID="tboxEmail" class="form-control EmailTextbox" runat="server" ValidationGroup="EmailInfo" Visible="False"></asp:TextBox>
                        <asp:RequiredFieldValidator ID="RequiredFieldValidator1" class="EmailErrText" runat="server" ErrorMessage="Please enter your okstate email address." ControlToValidate="tboxEmail" ValidationGroup="EmailInfo"></asp:RequiredFieldValidator>
                    </div>
                    <div class="LabelokstateText">
                        <asp:Label ID="lblMyPasswordLabel" class="col-form-label" runat="server" Text="Enter your okstate password: " Visible="False"></asp:Label>
                        <asp:TextBox ID="tboxPassword" class="form-control EmailTextbox" runat="server" TextMode="Password" ValidationGroup="EmailInfo"></asp:TextBox>
                        <asp:RequiredFieldValidator ID="RequiredFieldValidator2" class="EmailErrText" runat="server" ErrorMessage="Please enter your okstate password." ValidationGroup="EmailInfo" ControlToValidate="tboxPassword"></asp:RequiredFieldValidator>
                    </div>

                    <asp:Button ID="btnEmailCode" class="btn btn-dark btncodeassigned" runat="server" Text="Email My Code to Professor Strom" Visible="False" OnClick="btnEmailCode_Click" ValidationGroup="EmailInfo" />

                    <asp:Label ID="lblSuccess" class="EmailSuccessText" runat="server" Text=""></asp:Label>
                </div>
            </div>
        </div>
    </form>
</body>
</html>
