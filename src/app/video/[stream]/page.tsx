"use client"
import { Video } from "./_video/video";
import { Chat } from "./chat";
export default function mainVideo() {
	// TODO: Make here everything resizable with profiles
	return (
		<div className="h-full w-full">

			<div className="flex flex-row">
				<Video />
				<Chat />
			</div>
		</div >
	)
}
