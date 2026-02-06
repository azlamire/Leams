"use client"

import Input from '@mui/joy/Input';
import {IconButton} from '@mui/material';
import { useState, useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import { api } from '@/lib/api';
import { USER_SETTINGS } from '@/shared/constants';
import { Button } from '@mui/material';
import { Done, Close, Visibility, VisibilityOff } from '@mui/icons-material';
export default function settingsMain() {
  const [ test, setTest] = useState("");
  const [ show, setShow] = useState<"password" | "text">();
  const mutation = useMutation({
    mutationFn: () => {
      return api.post(USER_SETTINGS.NEXT_PUBLIC_GEN_USER_STREAM, {
        user_id: localStorage.getItem("access_token")
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Accept' : 'application/json',
        }
      })
    },
    onError: () => {
      setTimeout(() => mutation.reset(),3000)
    },

    onSuccess: (stream_id) => {
      setTest(stream_id.data)
      console.log(test)
      setTimeout(() => mutation.reset(),3000)

    },
  })
  return (
		<div className="h-full w-full flex items-center justify-center p-5">
			<div className="flex flex-row gap-5">
        <div>
          <label>
            Stream key
          </label>
        </div>
        <div>
            <Input
              readOnly
              className='relative z-0'
              type={show}
              color="neutral"
              value={test}
              size="lg"
              variant="outlined"
              endDecorator={
                <IconButton className="absolute cursor-pointer z-10" onClick={() => setShow((show) => !show)} tabIndex={-1}>
                  {show === "text" ? <VisibilityOff fontSize="small" /> : <Visibility fontSize="small" />}
                </IconButton>
            }
          >
            </Input>
            <Button variant='outlined' onClick={() => navigator.clipboard.writeText(test)}>Copy</Button>
            <Button 
              variant='outlined'
              onClick={() => mutation.mutate()}> { mutation.isSuccess ? <Done /> 
                  : mutation.isError ? <Close /> : "Reset"
                }
            </Button>
        </div>
			</div>
		</div >
	)
}

