function getLanguage() {
    if (navigator.userLanguage) {
        return navigator.userLanguage;
    } else if (navigator.language) {
        return navigator.language;
    } else if (navigator.browserLanguage) {
        return navigator.browserLanguage;
    } else if (navigator.systemLanguage) {
        return navigator.systemLanguage;
    } else {
        return "en-US";
    }
}
function dateTimeToHtml5(dateTime, language, options) {
    if (!language) {
        languge = getLanguage();
    }
    if (!options) {
        options = {year:"numeric", month:"2-digit", day:"2-digit", hour12:"false"};
    }
    var localized = new Date(dateTime);
    localized = localized.toLocaleTimeString(language, options);
    return  '<time datetime="' + dateTime + '">' + localized + '</time>';
}
