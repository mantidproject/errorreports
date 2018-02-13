function paraviewVerLink(version) {
    if (version === "0") {
        return "disabled";
    }
    var content = "<a href='http://www.paraview.org/Wiki/ParaView_Release_Notes";
    if (version === "3.98.1") {
        return content + "#ParaView_3.98.1_.28February_2013.29'>3.98.1</a>";
    }
    return version;
}

function mantidVerType(version) {
    if (/^\d+\.\d+\.\d+$/.test(version)) {
        return "stable";
    } else {
        // can't tell the difference between nightly and unstable
        return "develop";
    }
}

function mantidVerShaLink(version, sha1) {
    var content = "<a href='https://github.com/mantidproject/mantid/";
    if (mantidVerType(version) === "stable") {
        content += "releases/tag/v" + version;
    } else {
        content +=  "commit/" + sha1;
    }
    return content  + "'>" + version + "</a>";
}

function md5Link(base, md5) {
    return '<a href="' + base + md5 +'">' + md5.substring(0,10) + '</a>';
}
