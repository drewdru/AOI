// include script.js
// Qt.include("test.js")

function replaced(str, p1, p2) {
    var res = encodeURI(str);
    res = res.replace(p1,p2);
    res = decodeURI(res);
    return res;
}

function loadProcessingImage() {
    ice.loadProcessingImage();
}

function queueMe(response) {
    console.log('!!!!Defined Function Called: ' + response + "\n");
}

function onLoad() {
    console.log("onLoad start==================");
    // console.log('!!!! testGetData PASS DATA:    ' + ice + "\n")
    ice.enqueue('#version 1', queueMe);
    ice.enqueue('#test', function test() { console.log('!!!! RAN ME TO ANONYMOUSE');});
    ice.enqueue('#asdft', function newtest(reply) { console.log('!!!! PASS DATA:    ' + reply + "\n");});
    console.log("     =========================");
    ice.processResponses();
    console.log("onLoad done==================");
    loadProcessingImage();
}

function changeHue(value, isOriginalImage) {
    ice.changeHue(value, isOriginalImage);
}

function toGrayscale(isOriginalImage) {
    ice.toGrayscale(isOriginalImage);
}

function openFile(fileUrl) {
    var filePath = replaced(fileUrl, "file://", "");
    ice.openFile(filePath);
}

function saveFile(fileUrl) {
    var filePath = replaced(fileUrl, "file://", "");
    ice.saveFile(filePath);
}