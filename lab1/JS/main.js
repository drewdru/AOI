// include script.js
// Qt.include("test.js")

function replaced(str, p1, p2) {
    var res = encodeURI(str);
    res = res.replace(p1,p2);
    res = decodeURI(res);
    return res;
}

function loadProcessingImage() {
    mainController.loadProcessingImage();
}

// function queueMe(response) {
//     console.log('!!!!Defined Function Called: ' + response + "\n");
// }

function onLoad() {
    // console.log("onLoad start==================");
    // // console.log('!!!! testGetData PASS DATA:    ' + mainController + "\n")
    // mainController.enqueue('#version 1', queueMe);
    // mainController.enqueue('#test', function test() { console.log('!!!! RAN ME TO ANONYMOUSE');});
    // mainController.enqueue('#asdft', function newtest(reply) { console.log('!!!! PASS DATA:    ' + reply + "\n");});
    // console.log("     =========================");
    // mainController.processResponses();
    // console.log("onLoad done==================");
    loadProcessingImage();
}

function openFile(fileUrl) {
    var filePath = replaced(fileUrl, "file://", "");
    mainController.openFile(filePath);
}

function saveFile(fileUrl) {
    var filePath = replaced(fileUrl, "file://", "");
    mainController.saveFile(filePath);
}