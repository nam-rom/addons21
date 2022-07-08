/*
 *
 * Licensed under the MIT License
 *
 * Copyright(c) 2010 Alexis Deveria
 * Copyright(c) 2010 Pavol Rusnak
 * Copyright(c) 2010 Jeff Schiller
 * Copyright(c) 2010 Narendra Sisodiya
 * Copyright(c)  2012 Mark MacKay
 * Copyright(c) 2020 Yoonchae Lee
 * 
 */


window.ankiAddonSetImg = function (data, type) {
    if (type == "svg") {
        methodDraw.loadFromString(data)
    } else {
        setImage = function (img_width, img_height) {
            svgCanvas.setResolution(img_width, img_height)
            $("#canvas_width").val(img_width)
            $("#canvas_height").val(img_height)
            var newImage = svgCanvas.addSvgElementFromJson({
                "element": "image",
                "attr": {
                    "x": 0,
                    "y": 0,
                    "width": img_width,
                    "height": img_height,
                    "id": svgCanvas.getNextId(),
                    "style": "pointer-events:inherit"
                }
            });
            svgCanvas.setHref(newImage, data);
            svgCanvas.selectOnly([newImage]);
            svgCanvas.alignSelectedElements("m", "page")
            svgCanvas.alignSelectedElements("c", "page")
            svgCanvas.clearSelection();
            methodDraw.updateCanvas();
        }
        // put a placeholder img so we know the default dimensions
        var img_width = 100;
        var img_height = 100;
        var img = new Image()
        img.src = data
        document.body.appendChild(img);
        img.onload = function () {
            img_width = img.offsetWidth
            img_height = img.offsetHeight
            setImage(img_width, img_height);
            document.body.removeChild(img);
        }
    };
}

window.ankiAddonSaveImg = function () {
    svgCanvas.clearSelection()
    svg_str = svgCanvas.getSvgString()
    pycmd("svg_save:" + svg_str)
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function wait_until_pycmd(cb) {
    while (typeof pycmd !== "function") {
        await sleep(100);
    }
    cb();
}

window.addEventListener("load", function (e) {
    wait_until_pycmd(function () { pycmd("img_src") });
})