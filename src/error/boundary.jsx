import React from 'react'
import { Error } from './error'

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }
  
  componentDidCatch(error, info) {
    console.error(error, info.componentStack)
  }

  render() {
    if (this.state.hasError) 
      return <Error error={this.state.error} />
    
    return this.props.children
  }
}