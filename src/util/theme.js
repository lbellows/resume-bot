import { createTheme } from '@mui/material'

const tmpTheme = createTheme({
  palette: {
    primary: { main: '#743DBC' }, //Grape
    secondary: { main: '#EFDAFE' }, //Vibrant Grape20
    text: { primary: '#1B1A1A' },
    background:{ default: '#FBFAF8'},
    error: {main: '#BB0000' },
    success: {main: '#4FB209' },
    white: { main: '#FFFFFF' }
  },
  typography: { 
    h1: { fontWeight: 700, lineHeight: '100px', fontSize: '96px' },
    h2: { fontWeight: 700, lineHeight: '84px', fontSize: '80px' },
    h3: { fontWeight: 700, lineHeight: '68px', fontSize: '64px' },
    h4: { fontWeight: 700, lineHeight: '52px', fontSize: '48px' },
    h5: { fontWeight: 700, lineHeight: '34px', fontSize: '32px' },
    h6: { fontWeight: 700, lineHeight: '28px', fontSize: '24px' }
  },
  shadows: [
    'none',
    '0px 6px 6px 0px rgba(239, 237, 231, 0.50)', //header
    '0px 4px 12px 4px rgba(27, 26, 26, 0.10)', //main widgets
    ...Array(30).fill('none'), //mui bug fix
  ]
})

export const theme = createTheme(tmpTheme, {
  palette:{
    deepGrape: tmpTheme.palette.augmentColor({color: { main: '#3B0862' }, name: 'deepGrape'}),
    vibrantGrape: tmpTheme.palette.augmentColor({color: { main: '#AD44FB' }, name: 'vibrantGrape'}),
    lemon: tmpTheme.palette.augmentColor({color: { main: '#F8D84E' }, name: 'lemon'}),
    oyster: tmpTheme.palette.augmentColor({color: { main: '#EAE2F5' }, name: 'oyster'}),
    oyster40: tmpTheme.palette.augmentColor({color: { main: '#F7F3FB' }, name: 'oyster40'}),
    grapefruit: tmpTheme.palette.augmentColor({color: { main: '#EA6E6E' }, name: 'grapefruit'}),
    aqua: tmpTheme.palette.augmentColor({color: { main: '#05969F' }, name: 'aqua'}),
    insGray: tmpTheme.palette.augmentColor({color: { main: '#F2F2F2' }, name: 'insGray'}),
    insBlack: tmpTheme.palette.augmentColor({color: { main: '#1B1A1A' }, name: 'insBlack'}),
    beige: tmpTheme.palette.augmentColor({color: { main: '#FBFAF8' }, name: 'beige'}) 
  }
})

