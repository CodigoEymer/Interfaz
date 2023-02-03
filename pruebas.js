
const copyToClipboard = str => {
    if (navigator && navigator.clipboard && navigator.clipboard.writeText)
      return navigator.clipboard.writeText(str);
    return Promise.reject("The Clipboard API is not available.");
};

document.getElementById('export')
document.getElementById('export')
{"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-76.518016,3.43216],[-76.529775,3.443641],[-76.534195,3.432503],[-76.518016,3.43216]]]}}]}


var aux = document.getElementById('export').innerHTML;
aux.select();
document.execCommand('copy');
alert("copiadoo!!")