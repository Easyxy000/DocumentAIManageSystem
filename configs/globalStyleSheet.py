GLOBAL_STYLE_SHEET = """
QLineEdit{
    border: 1px solid #a1a3a4;
}
QPushButton{
    border-width:4px;
    border-image:url(images/button.png)  4 4 4 4 stretch stretch;
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
#menuItem{
    border-top: 2px solid #7c8394;
    background-color: #96add4;
    background-position: center center;
    background-origin: content;
    background-repeat: none;
    color : #ffffff;
    font-size:16px;
}
#menuItem:focus{
    background-color: #8095ba;
}
#dropBar{

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
    max-height:40px;
    min-width:50%;
}

QHeaderView{
    padding:0;
    margin:0;

}
QHeaderView::section { 
    background-color:#f7f9fc;
    border: 0; 
    color: #6d6f72; 
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