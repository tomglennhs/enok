import { ChakraProvider, extendTheme } from '@chakra-ui/react'
import {SWRConfig} from "swr";
import fetchApi from "../lib/fetch";

const theme = extendTheme({
    fonts: {
        body: "'IBM Plex Sans', system-ui, sans-serif",
        heading: "'IBM Plex Sans', system-ui, sans-serif",
        mono: "'IBM Plex Mono', monospace",
    },
})

function MyApp({ Component, pageProps }) {
  return (
      <SWRConfig value={{ fetcher: fetchApi }}>
      <ChakraProvider theme={theme}>
        <Component {...pageProps} />
      </ChakraProvider>
      </SWRConfig>
  )
}

export default MyApp
