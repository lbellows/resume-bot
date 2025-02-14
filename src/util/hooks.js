/* eslint-disable react-hooks/exhaustive-deps */

import { useEffect, useState } from 'react'
import { useApp } from './context'
import { httpGet, httpPost } from './api'

const defaultConfig = {
  defaultVal: null, 
  dependencies: [], 
  condition: true, 
  returnSetter: false,
  postData: null
}

/**
 * 
 * @param {string} url 
 * @param {object} config - set postData property to make this a post
 * @returns 
 */
export const useApiData = (
  url,
  config = defaultConfig
) => {

  const { 
    defaultVal,
    dependencies,
    condition,
    returnSetter,
    postData
  } = {
    ...defaultConfig,
    ...config
  }

  const [data, setData] = useState(defaultVal)
  const context = useApp()

  useEffect(() => {
    let isMounted = true
    const cntrl = new AbortController()

    try{
      if (condition) {
        const getData = async () => {
          let res = null
          if(isMounted && !cntrl.signal.aborted){
            if(postData)
              res = (await httpPost(url, postData, cntrl.signal))
            else
              res = (await httpGet(url, cntrl.signal))
          }
          if(isMounted && !cntrl.signal.aborted){
            if(res.error)
              context.setError(res.error)
            else
              setData(res.data)
          }
        }
        getData()
      }
    }catch(e){
      console.error('error in useApi hook', e)
      context.setError(e)
    }

    return () => {
      isMounted = false
      cntrl.abort()
    }
  }, dependencies)

  if (returnSetter)
    return [data, setData]

  return data
}

export const useAsync = (
  asyncFunc, 
  config = defaultConfig
) => {

  const { 
    defaultVal,
    dependencies,
    condition,
    returnSetter
  } = {
    ...defaultConfig,
    ...config
  }
  
  const [data, setData] = useState(defaultVal)

  useEffect(() => {
    let isMounted = true

    if (condition) {
      const getData = async () => {
        let res = null
        if (isMounted)
          res = await asyncFunc()
        if (isMounted)
          setData(res)
      }
      getData()
    }

    return () => {
      isMounted = false
    }
  }, dependencies)

  if (returnSetter)
    return [data, setData]

  return data
}