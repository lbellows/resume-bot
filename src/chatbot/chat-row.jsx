import { Box, Stack, Typography, Avatar } from '@mui/material'
// import { useApp } from '../util'
import Markdown from 'react-markdown'

const UserChat = ({config}) => {
  // const context = useApp()

  const styles = {
    bgcolor: "color-mix(in srgb, #0056b3 70%, white)",
    borderRadius: '16px 16px 0px 16px',
    maxWidth: 360,
    padding: 1,
  }

  return <Stack direction='row' sx={{alignSelf: 'flex-end'}}>
    <Box sx={styles}>
      <Typography component='span' fontWeight={700} fontSize={12}>{config.name}</Typography>
      <Typography component='span' fontSize={12} ml={1}>{config.time}</Typography>
      <div>{config.text}</div>
    </Box>
    
  </Stack>
}

const BotChat = ({config}) => {
  const styles = {
    bgcolor: '#FFF',
    borderRadius: '16px 16px 16px 0px',
    maxWidth: 360,
    padding: 1,
    alignSelf: 'start'
  }

  return <Stack direction='row'>
    <Avatar sx={{width:32, height: 32, fontSize:16, borderRadius:'16px', ml:1, pt:'4px'}}>RB</Avatar>
    <Box sx={styles}>
      <Typography component='span' fontWeight={700} fontSize={12}>{config.name}</Typography>
      <Typography component='span' fontSize={12} ml={1}>{config.time}</Typography>
      <Markdown>{config.text}</Markdown>
    </Box>
  </Stack>
}

export const ChatRow = ({config}) => 
  config.isUser ? 
    <UserChat config={config} /> : 
    <BotChat config={config} />