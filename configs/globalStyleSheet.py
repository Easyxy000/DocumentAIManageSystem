GLOBAL_STYLE_SHEET = """
QLabel,QCheckBox, QComboBox, QRadioButton{
    color:#6d6f72;
    font-size:14px;
}
QCheckBoxP{
    padding-top:5px;
    padding-bottom:5px;
}
QLineEdit{
    border: 1px solid #a1a3a4;
    height:25px;
}
QPushButton{
}
QRadioButton{
    padding:0;
    margin: 0 5px;
}
#topBarSearchLine{
    border:0;
    background-image: url(images/searchLine.png);
    background-position: center center;
    background-origin: content;
    background-repeat: none;
}
#topBarSearchBtn{
    border:0;
    background-image: url(images/searchBtn.png);
    background-position: center center;
    background-origin: content;
    background-repeat: none;
}

#formLabel{
    padding-right:10px;
    min-width:150px;
}
#button_default,
#button_primary,
#button_success,
#button_info,
#button_warning,
#button_danger{
    border-radius:8px;
    font-size:16px;
    color:#fff;
    min-height:33px;
    max-height:33px;
}
#button_default{
    background-color:#6d6f72;
}
#button_default:hover{
    background-color:#4a4b4d;
}
#button_primary{
    background-color: #96add4;
}

#button_primary:hover{
    background-color:#8095ba;
}
#button_success{
    background-color:#5cb85c;
}
#button_success:hover{
    background-color:#449d44;
}
#button_info{
    background-color:#5bc0de;
}
#button_info:hover{
    background-color:#31b0d5;
}
#button_warning{
    background-color:#f0ad4e;
}
#button_warning:hover{
    background-color:#ec971f;
}
#button_danger{
    background-color:#d9534f;
}
#button_danger:hover{
    background-color:#c9302c;
}

#resetBtn{
    border-radius:10px;
    font-size:16px;
    color:#fff;
    background-color: #6d6f72;
    min-height:38px;
    max-height:38px;
}

#mainWindow{
    background-color:#f7f9fc;
}

#topBorderNarrowBtn{
    border:0;
    border-image: none;
    background-image: url(images/narrow.png);
    background-position: center center;
    background-origin: content;
    background-repeat: none;
    width: 15px;
    height:15px;
}
#topBorderAmplificationBtn{
    border:0;
    border-image: none;
    background-image: url(images/amplification.png);
    background-position: center center;
    background-origin: content;
    background-repeat: none;
    width: 15px;
    height:15px;
}
#topBorderCloseBtn{
    border:0;
    border-image: none;
    background-image: url(images/close.png);
    background-position: center center;
    background-origin: content;
    background-repeat: none;
    width: 15px;
    height:15px;
}

#logoBox{
    background-color: #96add4;
    background-image: url(images/logo.png);
    background-position: center center;
    background-origin: content;
    background-repeat: none;
}
#menuItem, #menuItem:focus{
    border-top: 2px solid #7c8394;
    background-color: #96add4;
    background-position: center center;
    background-origin: content;
    background-repeat: none;
    color : #ffffff;
    font-size:16px;
}
#dropBar{

}
#formTitle{
    color:#666;
    font-size:16px;
}
#fileChooseBtn{
    background-color:#e3d394;
    border-image:none;
    border:0;
    width:70px;
    height 35px;
    color:#FFFFFF;
    font-size:18px;
}
#checkedGroup{
    min-height:40px;
    min-width:50%;
}
#checkedTimeGroup{
    min-height:40px;
    min-width:250px;
}
QHeaderView{
    padding:0;
    margin:0;

}
QHeaderView::section { 
    background-color:#f7f9fc;
    border: 0; 
    color: #666;
}
QTableView::item{
    height:80px;
    min-height:80px;
}
QTableView::item,#QTableViewDelegate{ 
    background-color:#f7f9fc;
    border:0;
}

QTableView::item:hover { 
    background-color: #dae2f0;
}
#tableViewOpenBtn{
    margin: 0 auto;
}


#tableViewPrimaryBtn, #tableViewWarningBtn{
    border-radius:5px;
    font-size:12px;
    color:#fff;
    min-height:25px;
    max-height:25px;
    padding: 0 3px;
}
#tableViewPrimaryBtn{
    background-color: #96add4;
}
#tableViewPrimaryBtn:hover{
    background-color:#8095ba;
}
#tableViewWarningBtn{
    background-color:#f0ad4e;
    
}
#tableViewWarningBtn:hover{
    background-color:#ec971f;
}
#bottomBar{
    background-color:#dae2f0;
}
#bottomTitle{
    font-size:14px;
    color:#564d4d;
}
#bottomSmallTitle{
    font-size:12px;
    color:#564d4d;
}
#checkUpdate{
    color:#564d4d;
    font-size:14px;
    background-image:url(images/checkUpdate.png);
    background-position: left center;
    background-origin: content;
    background-repeat: none;
}
"""