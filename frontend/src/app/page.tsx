"use client"

import { api } from "@/lib/api";
import Link from "next/link";
import { MAIN } from "@/shared/constants";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useInView } from "react-intersection-observer";
import { MainCategory } from "./_components/main-section/category";
import { UpSide } from "./_components/nav-section//UpSide";
import { LeftSide } from "./_components/left-section/left-main";
import { MainStreams } from "./_components/main-section/streams";
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
	)
}
