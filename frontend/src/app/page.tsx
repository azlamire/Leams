"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useInView } from "react-intersection-observer";
import { api } from "@/lib/api";
import { MAIN } from "@/shared/constants";
import { LeftSide } from "./_components/left-section/left-main";
import { MainCategory } from "./_components/main-section/category";
import { MainStreams } from "./_components/main-section/streams";
import { UpSide } from "./_components/nav-section//UpSide";
export default function MainPage() {
	return (
		<div className="h-screen">
			<UpSide />
			<div className="inline-flex h-full w-full">
				<LeftSide />
				<main className="w-full z-0">
					<MainStreams />
				</main>
			</div>
		</div>
	);
}
