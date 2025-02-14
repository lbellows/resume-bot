import { Box, Typography } from '@mui/material'

export const Widget = ({children, title, css={} }) => {
  const wrapperStyles = {
    // mt: 2,
    boxShadow: 2,
    px:2,
    py:3,
    borderRadius: 0,
    border: '1px solid #E8E8E8',
    backgroundColor: 'white.main',
    ...css
  }

  return  <Box sx={wrapperStyles} >
    {title && <Typography variant='h6'>{title}</Typography>}
    {children}
  </Box>

}