
import { useLayoutEffect, useRef, useState } from 'react'
import { Widget } from '../shared'
import { getCurrentTime, httpPost } from '../util'
import { Stack, Box, Typography, Button, TextField } from '@mui/material'
import { ArrowForward, Refresh } from '@mui/icons-material'
import { ChatRow } from './chat-row'
import AccessTimeIcon from '@mui/icons-material/AccessTime'

export const Chatbot = () => {
  // const context = useApp()

  const historyInit = [{
    time: getCurrentTime(),
    name: 'ResumeBot',
    text: `Hi there, AI assistant here to help!`,
    isUser: false,
    sources: []
  }]

  const [chatHistory, setChatHistory] = useState(historyInit)
  const [chatInput, setChatInput] = useState('')
  const chatRef = useRef(null)
  const [apiLoading, setApiLoading] = useState(false)

  const chatHandler = async () => {
    if (!chatInput)
      return

    setApiLoading(true)

    const newUserChat = {
      time: getCurrentTime(),
      name: 'You',
      text: chatInput,
      isUser: true,
      role: 'user',
      content: chatInput
    }
    const chatWithUser = [...chatHistory, newUserChat]
    setChatHistory(chatWithUser)

    const onlyUserChats = chatWithUser
      .filter(c => c.isUser)
      .map(({ content, role }) => ({ content, role }))

    const chat = await httpPost('/api/chat', { chats: onlyUserChats })

    const newBotChat = {
      time: getCurrentTime(),
      name: 'ResumeBot',
      text: chat.data.data,
      isUser: false,
      role: 'system',
      content: chat.data.data
      // sources: chat.data.sources
    }
    const chatWithBot = [...chatWithUser, newBotChat]
    setChatInput('')
    setChatHistory(chatWithBot)
    setApiLoading(false)
  }

  useLayoutEffect(() => {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    });
  }, [chatHistory])

  const refreshHandler = () => {
    setChatHistory(historyInit)
  }

  return <>
    {/* width 570px */}
    <Widget css={{ bgcolor: '#FBF9FD', flex: 1 }}>
      {/* chat history */}
      <Stack spacing={2} sx={{ overflowY: 'auto' }} ref={chatRef}>

        {chatHistory.map((ch, idx) => <ChatRow config={ch} key={idx} />)}
        {apiLoading && <Typography fontSize={12} color='#242424'>
          <AccessTimeIcon />
          Searching for details... Generating answers for you.
        </Typography>
        }
      </Stack>
    </Widget>
    {/* input area */}
    <Box sx={{ bgcolor: '#F7F3FB', px: 2, pt: 2, pb: 1, boxShadow: 2 }}>
      <TextField value={chatInput}
        onChange={(e) => setChatInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key == 'Enter')
            chatHandler()
        }}
        disabled={apiLoading}
        label="Ask me about my resume..."
        variant="outlined"
        size='small' 
        fullWidth
        sx={{ bgcolor: apiLoading ? 'insGray.dark' : 'initial' }}
      />
      <Box justifyContent='space-between' display='flex'>
        <Button onClick={refreshHandler} variant="text" startIcon={<Refresh />}>
          New Chat
        </Button>
        <Button onClick={chatHandler} variant="text" endIcon={<ArrowForward />}>
          Send
        </Button>
      </Box>
    </Box>
  </>
}