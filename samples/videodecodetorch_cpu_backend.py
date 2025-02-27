import datetime
import sys
import argparse
import os.path
import torch
import pyRocVideoDecode.decodercpu as dec
import pyRocVideoDecode.demuxer as dmx


def Decoder(
        input_file_path,
        output_file_path,
        device_id,
        mem_type,
        crop_rect):

    # demuxer instance
    demuxer = dmx.demuxer(input_file_path)

    # get the used coded id
    codec_id = dec.GetRocDecCodecID(demuxer.GetCodecId())

    # decoder instance
    viddec = dec.decodercpu(       
        codec_id,
        device_id,
        mem_type)

    # Get GPU device information
    cfg = viddec.GetGpuInfo()

    # check if codec is supported
    if (viddec.IsCodecSupported(device_id, codec_id, demuxer.GetBitDepth()) == False):
        print("ERROR: Codec is not supported on this GPU " + cfg.device_name)
        exit()

    #  print some GPU info out
    print("\ninfo: Input file: " +
          input_file_path +
          '\n' +
          "info: Using GPU device " +
          str(device_id) +
          " - " +
          cfg.device_name +
          "[" +
          cfg.gcn_arch_name +
          "] on PCI bus " +
          str(cfg.pci_bus_id) +
          ":" +
          str(cfg.pci_domain_id) +
          "." +
          str(cfg.pci_device_id))
    print("info: decoding started, please wait! \n")

    # -----------------
    # The decoding loop
    # -----------------
    n_frame = 0
    total_dec_time = 0.0

    while True:
        start_time = datetime.datetime.now()
        packet = demuxer.DemuxFrame()
        n_frame_returned = viddec.DecodeFrame(packet)

        for i in range(n_frame_returned):
            viddec.GetFrameYuv(packet)

            # Yuv (NV12) Plane torch tensor
            yuv_tensor = torch.from_dlpack(packet.ext_buf[0].__dlpack__(packet))

            # TODO: some tensor work

            # save tensors to file, with original decoded Size
            if (output_file_path is not None):
                viddec.SaveFrameToFile(
                    output_file_path,
                    yuv_tensor.data_ptr())

            # release frame
            viddec.ReleaseFrame(packet)

        # measure after completing a whole frame
        end_time = datetime.datetime.now()
        time_per_frame = end_time - start_time
        total_dec_time = total_dec_time + time_per_frame.total_seconds()

        # increament frames counter
        n_frame += n_frame_returned

        if (packet.bitstream_size <= 0):  # EOF: no more to decode
            break

    # beyond the decoding loop
    n_frame += viddec.GetNumOfFlushedFrames()

    print("info: Total frame decoded: " + str(n_frame))

    if (output_file_path is None):
        if (n_frame > 0 and total_dec_time > 0):
            time_per_frame = (total_dec_time / n_frame) * 1000
            frame_per_second = n_frame / total_dec_time
            print("info: avg decoding time per frame: " +"{0:0.2f}".format(round(time_per_frame, 2)) + " ms")
            print("info: avg frame per second: " +"{0:0.2f}".format(round(frame_per_second,2)) +"\n")
        else:
            print("info: frame count= ", n_frame)

    # print tensor details
    print("Tensor Shape:   ", packet.ext_buf[0].shape)
    print("Tensor Strides: ", packet.ext_buf[0].strides)
    print("Tensor dType:   ", packet.ext_buf[0].dtype)
    print("Tensor Device:  ", packet.ext_buf[0].__dlpack_device__(), "\n")


if __name__ == "__main__":

    # get passed arguments
    parser = argparse.ArgumentParser(
        description='PyRocDecode Video Decode Arguments')
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help='Input File Path - required',
        required=True)
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='Output File Path - optional',
        required=False)
    parser.add_argument(
        '-d',
        '--device',
        type=int,
        default=0,
        help='GPU device ID - optional, default 0',
        required=False)
    parser.add_argument(
        '-m',
        '--mem_type',
        type=int,
        default=1,
        help='mem_type of output surfce - 0: Internal 1: dev_copied 2: host_copied 3: MEM not mapped, optional, default 0',
        required=False)
    parser.add_argument(
        '-crop',
        '--crop_rect',
        nargs=4,
        type=int,
        help='Crop rectangle (left, top, right, bottom), optional, default: no cropping',
        required=False)

    try:
        args = parser.parse_args()
    except BaseException:
        sys.exit()

    # get params
    input_file_path = args.input
    output_file_path = args.output
    device_id = args.device
    mem_type = args.mem_type
    crop_rect = args.crop_rect

    # handel params
    mem_type = 1
    if not os.path.exists(input_file_path):  # Input file (must exist)
        print("ERROR: input file doesn't exist.")
        exit()

    # torch GPU
    print("\nPyTorch Using: ", torch.cuda.get_device_name(0))

    Decoder(
        input_file_path,
        output_file_path,
        device_id,
        mem_type,
        crop_rect)
