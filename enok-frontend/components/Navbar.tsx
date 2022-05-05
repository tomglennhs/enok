import {Box, Flex, Heading, Icon, Text} from "@chakra-ui/react";
import * as React from "react";
import {ReactElement} from "react";
import Link from "next/link";

const Navbar = () => (
    <Box minH={"100vh"} w={"7.5vw"} backgroundColor={"gray.900"}>
        <Heading color={"white"} mb={2}>Enok</Heading>
        {/* TODO: Switch out icons */}
        {/*<NavButton label="Home" href="/" icon={HomeIcon}/>*/}
        {/*<NavButton label="Printers" href="/printers" icon={HomeIcon}/>*/}
        {/*<NavButton label="Jobs" href="/jobs" icon={HomeIcon}/>*/}

    </Box>
)

const NavButton = ({icon, label, href}: {icon, label: string, href: string}) => (
    <Link href={href}>
    <Flex borderBottom="1px" borderBottomColor="white" color="white" alignItems={"center"} flexDirection={"column"}>
        <Icon w="100%" m={2} as={icon} backgroundColor={"none"} aria-label={label}/>
        <Text >{label}</Text>
        </Flex>
    </Link>
)

export default Navbar