import { ChakraProvider, extendTheme } from '@chakra-ui/react'

const theme = extendTheme({
    fonts: {
        body: "'IBM Plex Sans', system-ui, sans-serif",
        heading: "'IBM Plex Sans', system-ui, sans-serif",
        mono: "'IBM Plex Mono', monospace",
    },
})

function MyApp({ Component, pageProps }) {
  return (
      <ChakraProvider theme={theme}>
        <Component {...pageProps} />
      </ChakraProvider>
  )
}

export default MyApp
