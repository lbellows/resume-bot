const getErrorResponse = (error) => {
  if(!error?.message.includes('aborted'))
    console.error('HTTP error', error)
  return {
    response: { ok: false, status: 500 },
    data: error,
    error: true
  }
}

const formatResponse = async (res) => {
  if (!res) throw Error('Unknown response')
  const response = res.clone()
  if (!res.ok) {
    const errorText = await res.text()
    console.error('HTTP error: ' + errorText, response)
    return {
      response,
      data: errorText,
      error: true
    }
  }
  const json = await res.json()
  return {
    response,
    data: json
  }
}

const getUrl = (url) => (location.hostname == 'localhost' ? 'https://kind-coast-0a2b3dc0f.4.azurestaticapps.net' : '') + url

export const httpGet = async (relApiUrl, signal) => {

  try{
    const headers = {}
    var res = await fetch(getUrl(relApiUrl), {
      method: 'GET',
      headers,
      signal
    })

  } catch (e) {
    return getErrorResponse(e)
  }

  return formatResponse(res)
}

export const httpPost = async (relApiUrl, data, signal) => {
  try {
    const headers = {}
    var res = await fetch(getUrl(relApiUrl), {
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      method: 'POST',
      body: JSON.stringify(data),
      signal
    })
  } catch (e) {
    return getErrorResponse(e)
  }
  return formatResponse(res)
}