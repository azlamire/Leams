import { motion } from "motion/react";

import VideoPlayer from "./video-player";
export function Video() {
	return (
		<motion.div>
			<VideoPlayer src="http://localhost:80/hls/test.m3u8" height={800} width={1300} />
		</motion.div>


	)
}
