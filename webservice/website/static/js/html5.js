var elements = ['article', 'nav', 'section', 'header', 'aside', 'footer' ,'hgroup','time'];
for (var i=elements.length-1; i>=0; i--) {
	document.createElement(elements[i]);
}
