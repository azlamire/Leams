"use client";
import React, { useRef, useEffect } from "react";
import videojs from "video.js";
import "video.js/dist/video-js.css";
import "../../styles/video-js.css";

interface VideoPlayerProps {
	src: string;
	width: number;
	height: number;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ src, width, height }) => {
	const videoRef = useRef<HTMLVideoElement | null>(null);
	const playerRef = useRef<ReturnType<typeof videojs> | null>(null);

	useEffect(() => {
		if (videoRef.current) {
			playerRef.current = videojs(videoRef.current, {
				autoplay: true,
				controls: true,
				sources: [{ src, type: "application/x-mpegURL" }],
				width: width,
				height: height,
			});
		}
		return () => {
			if (playerRef.current) {
				playerRef.current.dispose();
				playerRef.current = null;
			}
		};
	}, [src]);

	return <video ref={videoRef} className="video-js" />;
};

export default VideoPlayer;
