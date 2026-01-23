"use client"
import { motion } from "motion/react";
import ReactPlayer from 'react-player'
import { useEffect } from "react";
import { useParams } from 'next/navigation';
export function Video() {
	const params = useParams();
	const slug = params.stream as string;
	useEffect(() => { console.log(slug) }, [])
	return (
		<motion.div>
			<ReactPlayer playing controls src={`http://localhost:80/hls/${slug}`} height={800} width={1300} />
		</motion.div>


	)
}
