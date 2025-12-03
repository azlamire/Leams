"use client"
import VideoPlayer from "./test";
import { motion } from "motion/react";
export default function mainVideo() {
	return (
		<div className="h-full w-full">

			<div className="chat">

			</div>

			<div>

			</div>

			<motion.div
				drag>
				<VideoPlayer src="http://localhost:80/hls/test.m3u8" />
			</motion.div>

		</div>
	)
}
