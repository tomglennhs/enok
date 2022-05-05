import Navbar from "../components/Navbar";
import {Flex, Heading, Image, Text, Box} from "@chakra-ui/react";
import useSWR from 'swr'

// TODO: Finish and relocate these interfaces
interface IUser {
    name: string
}

interface IPrinter {
    id: number
    name: string
}

export default function Dashboard() {
    const {data: user, error: userErr} = useSWR<IUser>('/users/me')
    const {data: printers, error: printersErr} = useSWR<IPrinter[]>('/printers/')

    if (!user) return <></>
    return (
        <Flex>
            <Navbar/>
            <Flex m={10} flexDirection={"column"}>
                <Heading as={'h1'}>Welcome, {user.name}</Heading>

                <Heading as={'h2'} fontSize={"2xl"} fontWeight={"regular"} color={"gray.500"} my={3}>Printers</Heading>
                <Flex>
                    {printers ? printers.map((p) => <PrinterCard printer={p} key={p.id}/>) : <></>}
                </Flex>
                {/* TODO: include a brief jobs section, and a section with stats on your prints */}
                <Flex>
                    <Flex flexDirection={"column"}>
                        <h1>Personal Stats</h1>
                        <p>Prints You've Queued: 5</p>
                        <p>Filament Remaining: 500g</p>
                    </Flex>
                    <Flex mx={"100px"} flexDirection={"column"}>
                        <h1>Global Stats</h1>
                        <p>Total Prints Monitored</p>
                        <p>Total Filament Used</p>
                    </Flex>
                </Flex>
            </Flex>
        </Flex>
    )
}

function PrinterCard({printer}: { printer: IPrinter }) {
    return (
        <Flex m={2} width={"16em"} borderColor={"gray"} borderWidth={"1px"} borderRadius={10} flexDirection={"column"}>
            {/* TODO: Give this box a fancy fallback background (maybe gradient?) while
            we wait for image/stream to load or if there isn't one */}
            <Box w={"100%"} h={"12em"} backgroundColor={"black"}>
                <Image w="100%" h={"100%"} objectFit={"contain"} alt={""} src={`/printers/${printer.id}/camera/jpg`}/>
            </Box>
            <Flex flexDirection={"column"} p={2}>
                <Text>{printer.name}</Text>
                <Text>Time remaining: 4h30m</Text>
                <Text>Prints in Queue: 1000000</Text>
            </Flex>
        </Flex>
    )
}