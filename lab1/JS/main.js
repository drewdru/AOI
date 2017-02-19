// include script.js
// Qt.include("test.js")

/**
 * Replace qml file url to path or another url
 * 
 * @param url: The file url
 * @param p1: The old prefix
 * @param p2: The new prefix
 */
function replaceUrlToPath(url, p1, p2) {
    var res = encodeURI(url);
    res = res.replace(p1,p2);
    res = decodeURI(res);
    return res;
}

/**
 * Replace processingImage.png
 */
function loadProcessingImage() {
    mainController.loadProcessingImage();
}

/**
 * The callback function
 */
function queueMe(response) {
    console.log('!!!!Defined Function Called: ' + response + "\n");
}

/**
 * The load data
 */
function onLoad() {
    // Example callback with controller
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

/**
 * Copy image to inImage.png
 * 
 * @param fileUrl: The qml file url
 */
function openFile(fileUrl) {
    var filePath = replaceUrlToPath(fileUrl, "file://", "");
    mainController.openFile(filePath);
}

/**
 * Copy processingImage.png to file
 * 
 * @param fileUrl: The qml file url
 */
function saveFile(fileUrl) {
    var filePath = replaceUrlToPath(fileUrl, "file://", "");
    mainController.saveFile(filePath);
}