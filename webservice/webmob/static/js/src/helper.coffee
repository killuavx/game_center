imgonerror = (img, src) ->
  img.onerror = null
  img.src = src
  false

this.imgonerror = imgonerror
