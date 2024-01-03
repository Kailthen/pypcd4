def decompress(inData, outLength):

    inLength = len(inData)
    outData = bytearray(outLength)
    inPtr = 0
    outPtr = 0
    ctrl = 0
    len_ = 0
    ref = 0

    while inPtr < inLength:

        ctrl = inData[inPtr]
        inPtr += 1

        if ctrl < (1 << 5):

            ctrl += 1
            if outPtr + ctrl > outLength:
                raise ValueError('Output buffer is not large enough')
            if inPtr + ctrl > inLength:
                raise ValueError('Invalid compressed data')
            while ctrl:
                outData[outPtr] = inData[inPtr]
                inPtr += 1
                outPtr += 1
                ctrl -= 1

        else:

            len_ = ctrl >> 5
            ref = outPtr - ((ctrl & 0x1f) << 8) - 1
            if inPtr >= inLength:
                raise ValueError('Invalid compressed data')
            if len_ == 7:

                len_ += inData[inPtr]
                inPtr += 1
                if inPtr >= inLength:
                    raise ValueError('Invalid compressed data')

            ref -= inData[inPtr]
            inPtr += 1
            if outPtr + len_ + 2 > outLength:
                raise ValueError('Output buffer is not large enough')
            if ref < 0:
                raise ValueError('Invalid compressed data')
            if ref >= outPtr:
                raise ValueError('Invalid compressed data')
            while len_ + 2:
                outData[outPtr] = outData[ref]
                ref += 1
                outPtr += 1
                len_ -= 1

    return outData